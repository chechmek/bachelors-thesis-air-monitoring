import psycopg2
from datetime import datetime

def get_db_connection(config):
    return psycopg2.connect(
        host=config['postgresql']['host'],
        port=config['postgresql']['port'],
        user=config['postgresql']['user'],
        password=config['postgresql']['password'],
        database=config['postgresql']['database_name']
    )

def save_metrics(conn, window_end_time, avg_temp, avg_humidity, avg_pm2_5, aqi):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO hourly_sensor_metrics 
            (window_end_time, avg_temp, avg_humidity, avg_pm2_5, aqi)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (window_end_time, avg_temp, avg_humidity, avg_pm2_5, aqi)
        )
        conn.commit() 