import psycopg2
import json
import os

def get_db_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config['postgresql']

def clean_tables():
    config = get_db_config()
    conn = psycopg2.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database_name']
    )
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DO $$ 
                DECLARE 
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                        EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
                    END LOOP;
                END $$;
            """)
        conn.commit()
        print("All tables have been cleaned successfully")
    except Exception as e:
        print(f"Error cleaning tables: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    clean_tables() 