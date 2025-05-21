import psycopg2
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {config_path}")
        raise

def get_db_connection(config):
    pg_config = config.get('postgresql')
    if not pg_config:
        logger.error("PostgreSQL configuration not found in config.json")
        raise ValueError("PostgreSQL configuration not found in config.json")

    logger.info(f"Connecting to PostgreSQL database '{pg_config.get('database_name')}' on {pg_config.get('host')}:{pg_config.get('port')}...")
    conn = psycopg2.connect(
        host=pg_config.get('host'),
        port=pg_config.get('port'),
        user=pg_config.get('user'),
        password=pg_config.get('password'),
        database=pg_config.get('database_name')
    )
    logger.info("Successfully connected to PostgreSQL.")
    return conn

def create_forecast_table(conn):
    try:
        with conn.cursor() as cur:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS forecast (
                id SERIAL PRIMARY KEY,
                date_forecasted TIMESTAMP WITHOUT TIME ZONE,
                date_target TIMESTAMP WITHOUT TIME ZONE,
                pm2_5 REAL
            );
            """
            cur.execute(create_table_query)
            conn.commit()
            logger.info("Table 'forecast' ensured to exist successfully.")
    except psycopg2.Error as e:
        logger.error(f"PostgreSQL error while creating forecast table: {e}")
        conn.rollback()
        raise

def create_metrics_table(conn):
    try:
        with conn.cursor() as cur:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS hourly_sensor_metrics (
                id SERIAL PRIMARY KEY,
                window_end_time TIMESTAMP WITHOUT TIME ZONE,
                avg_temp REAL,
                avg_humidity REAL,
                avg_pm2_5 REAL,
                aqi INTEGER
            );
            """
            cur.execute(create_table_query)
            conn.commit()
            logger.info("Table 'hourly_sensor_metrics' ensured to exist successfully.")
    except psycopg2.Error as e:
        logger.error(f"PostgreSQL error while creating metrics table: {e}")
        conn.rollback()
        raise

def init_database():
    conn = None
    try:
        config = load_config()
        conn = get_db_connection(config)
        
        create_forecast_table(conn)
        create_metrics_table(conn)
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            logger.info("PostgreSQL connection closed.")

if __name__ == "__main__":
    init_database()