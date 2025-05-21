import json
import logging
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metrics_service import calculate_metrics
from database_service import get_db_connection, save_metrics

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
        db_conn = get_db_connection(config)
        
        data_buffer = []
        logger.info("Starting sensor data analyzer...")
        
        for message in consumer:
            try:
                data = message.value
                data_buffer.append(data)
                
                if len(data_buffer) == 12:
                    window_end_time = datetime.fromisoformat(data_buffer[-1]['datetime'])
                    metrics = calculate_metrics(data_buffer)
                    
                    metrics_payload = {
                        "window_end_time": window_end_time.isoformat(),
                        "avg_temp": metrics['avg_temp'],
                        "avg_humidity": metrics['avg_humidity'],
                        "avg_pm2_5": metrics['avg_pm2_5'],
                        "aqi": metrics['aqi']
                    }
                    
                    producer.send(
                        config['kafka']['topics']['metrics'],
                        value=metrics_payload
                    )
                    
                    save_metrics(
                        db_conn,
                        window_end_time,
                        metrics['avg_temp'],
                        metrics['avg_humidity'],
                        metrics['avg_pm2_5'],
                        metrics['aqi']
                    )
                    
                    logger.info(f"Processed metrics for window ending at {window_end_time.isoformat()}")
                    data_buffer.clear()
            
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