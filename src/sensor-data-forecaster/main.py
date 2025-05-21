import json
import logging
from datetime import datetime, timedelta
from collections import deque
from kafka import KafkaConsumer, KafkaProducer
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prediction_service import load_model_and_scaler, predict_pm2_5, LOOK_BACK
from database_service import get_db_connection, save_forecast

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def create_kafka_consumer(config):
    return KafkaConsumer(
        config['kafka']['topics']['raw_sensor_data'],
        bootstrap_servers=config['kafka']['bootstrap_servers'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest'
    )

def create_kafka_producer(config):
    return KafkaProducer(
        bootstrap_servers=config['kafka']['bootstrap_servers'],
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )

def main():
    try:
        config = load_config()
        consumer = create_kafka_consumer(config)
        producer = create_kafka_producer(config)
        model, scaler = load_model_and_scaler()
        db_conn = get_db_connection(config)
        
        data_buffer = deque(maxlen=LOOK_BACK)
        latest_datetime = None
        last_forecast_hour = None
        
        logger.info("Starting sensor data forecaster...")
        
        for message in consumer:
            try:
                data = message.value
                pm2_5 = data['pm2_5']
                datetime_str = data['datetime']
                current_datetime = datetime.fromisoformat(datetime_str)
                
                data_buffer.append(pm2_5)
                latest_datetime = datetime_str
                
                if len(data_buffer) == LOOK_BACK:
                    current_hour = current_datetime.replace(minute=0, second=0, microsecond=0)
                    
                    if last_forecast_hour is None or current_hour > last_forecast_hour:
                        predictions = predict_pm2_5(list(data_buffer), model, scaler)
                        forecast_value = predictions[-1]
                        last_input_value = data_buffer[-1]
                        
                        date_forecasted = current_datetime
                        date_target = date_forecasted + timedelta(hours=1)
                        
                        forecast_payload = {
                            "date_forecasted": date_forecasted.isoformat(),
                            "date_target": date_target.isoformat(),
                            "pm2_5_last": float(last_input_value),
                            "pm2_5_forecasted": float(forecast_value)
                        }
                        
                        producer.send(
                            config['kafka']['topics']['forecast'],
                            value=forecast_payload
                        )
                        
                        save_forecast(
                            db_conn, 
                            date_forecasted, 
                            date_target, 
                            list(data_buffer), 
                            predictions.tolist(), 
                            float(forecast_value)
                        )
                        
                        logger.info(f"Made forecast for {date_target.isoformat()}: {forecast_value}")
                        last_forecast_hour = current_hour
            
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise
    finally:
        if 'db_conn' in locals():
            db_conn.close()
        if 'consumer' in locals():
            consumer.close()
        if 'producer' in locals():
            producer.close()

if __name__ == "__main__":
    main() 