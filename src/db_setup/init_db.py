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

def create_forecast_table():
    conn = None
    try:
        config = load_config()
        pg_config = config.get('postgresql')
        if not pg_config:
            logger.error("PostgreSQL configuration not found in config.json")
            return

        logger.info(f"Connecting to PostgreSQL database '{pg_config.get('database_name')}' on {pg_config.get('host')}:{pg_config.get('port')}...")
        conn = psycopg2.connect(
            host=pg_config.get('host'),
            port=pg_config.get('port'),
            user=pg_config.get('user'),
            password=pg_config.get('password'),
            database=pg_config.get('database_name')
        )
        logger.info("Successfully connected to PostgreSQL.")

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
        logger.error(f"PostgreSQL error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            logger.info("PostgreSQL connection closed.")

if __name__ == "__main__":
    create_forecast_table()