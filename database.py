import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
            sslmode=os.getenv("DB_SSLMODE")
        )
        return conn
    except Exception as e:
        print("❌ Error connecting to the database")
        print(e)
        return None
