import psycopg2
import os
from dotenv import load_dotenv
from contextlib import contextmanager


load_dotenv()

@contextmanager
def get_conn():
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD")
        )
        yield conn
    finally:
        conn.close()