# utils/db_connection.py
import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cricket.db")
DB_URL = f"sqlite:///{DB_PATH}"

def get_sqlite_connection(db_path=DB_PATH):
    return sqlite3.connect(db_path)

def get_engine(db_url=DB_URL):
    return create_engine(db_url, connect_args={"check_same_thread": False})

def run_query(query, params=None, db_url=DB_URL):
    """Run SELECT queries and return a DataFrame."""
    try:
        engine = get_engine(db_url)
        return pd.read_sql(query, engine, params=params)
    except Exception as e:
        print(f"[run_query Error] {e}")
        return pd.DataFrame()

def execute_query(query, params=None, db_path=DB_PATH):
    """Execute INSERT/UPDATE/DELETE safely (returns True/False)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(f"[execute_query Error] {e}")
        return False
    finally:
        conn.close()
