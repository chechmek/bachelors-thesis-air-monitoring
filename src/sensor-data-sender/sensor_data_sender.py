import json
import csv
import logging
from pathlib import Path
from kafka import KafkaProducer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    config_path = Path(__file__).parent.parent / 'config.json'
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in configuration file {config_path}")
        raise

def create_kafka_producer(bootstrap_servers):
    try:
        return KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    except Exception as e:
        logger.error(f"Failed to create Kafka producer: {e}")
        raise

def process_csv_and_send_to_kafka():
    config = load_config()
    producer = create_kafka_producer(config['kafka']['bootstrap_servers'])
    topic = config['kafka']['topics']['raw_sensor_data']
    
    csv_path = Path(__file__).parent / 'sensor_data.csv'
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    data = {
                        'ts': float(row['ts']),
                        'humidity': float(row['humidity']),
                        'temp': float(row['temp']),
                        'datetime': row['datetime'],
                        'pm2_5': float(row['pm2_5'])
                    }
                    producer.send(topic, value=data)
                    logger.info(f"Sent data: {data}")
                except Exception as e:
                    logger.error(f"Failed to send message: {e}")
                    continue
    except FileNotFoundError:
        logger.error(f"CSV file not found at {csv_path}")
        return
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        return
    finally:
        producer.flush()
        producer.close()

if __name__ == '__main__':
    try:
        process_csv_and_send_to_kafka()
        logger.info("Data processing completed successfully")
    except Exception as e:
        logger.error(f"Script failed: {e}") 