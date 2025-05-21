import psycopg2
from datetime import datetime
import logging

def get_db_connection(config):
    try:
        conn = psycopg2.connect(
            host=config['postgresql']['host'],
            port=config['postgresql']['port'],
            user=config['postgresql']['user'],
            password=config['postgresql']['password'],
            database=config['postgresql']['database_name']
        )
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        raise

def save_forecast(conn, date_forecasted, date_target, pm2_5_value):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO forecast (date_forecasted, date_target, pm2_5)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (date_forecasted, date_target, pm2_5_value)
            )
            forecast_id = cur.fetchone()[0]
            conn.commit()
            logging.info(f"Saved forecast with ID: {forecast_id}")
            return forecast_id
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to save forecast: {str(e)}")
        raise 