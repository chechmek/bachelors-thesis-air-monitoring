import json
import logging
from pathlib import Path
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

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

def create_topics():
    config = load_config()
    bootstrap_servers = config['kafka']['bootstrap_servers']
    topics = config['kafka']['topics']
    
    admin_client = None
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers
        )
        
        new_topics = []
        for topic_name in topics.values():
            new_topics.append(
                NewTopic(
                    name=topic_name,
                    num_partitions=1,
                    replication_factor=1
                )
            )
        
        if new_topics:
            try:
                admin_client.create_topics(
                    new_topics=new_topics,
                    validate_only=False
                )
                logger.info(f"Successfully created topics: {[topic.name for topic in new_topics]}")
            except TopicAlreadyExistsError as e:
                logger.info(f"Topics already exist: {[topic.name for topic in new_topics]}")
            except Exception as e:
                logger.error(f"Error creating topics: {e}")
                raise
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        raise
    finally:
        if admin_client:
            admin_client.close()

if __name__ == '__main__':
    try:
        create_topics()
        logger.info("Topic initialization completed")
    except Exception as e:
        logger.error(f"Script failed: {e}") 