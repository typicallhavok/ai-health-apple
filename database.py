# Database helper functions
import mysql.connector
from mysql.connector import pooling
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.122.11"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "apple_health"),
    "user": os.getenv("DB_USER", "havok"),
    "password": os.getenv("DB_PASS", "maria"),
}

pool = pooling.MySQLConnectionPool(
    pool_name="health_pool",
    pool_size=8,
    **DB_CONFIG
)

def get_connection():
    """Get a database connection from the pool"""
    return pool.get_connection()

def fetch_all(sql: str, params: tuple) -> List[Dict[str, Any]]:
    """Execute query and fetch all results"""
    cnx = get_connection()
    try:
        cur = cnx.cursor(dictionary=True)
        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        cnx.close()

def fetch_one(sql: str, params: tuple) -> Optional[Dict[str, Any]]:
    """Execute query and fetch one result"""
    rows = fetch_all(sql, params)
    return rows[0] if rows else None
