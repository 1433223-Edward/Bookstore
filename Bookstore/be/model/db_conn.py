import psycopg2
from psycopg2 import pool
import logging


class DBConn:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="bookstore",
            user="postgres",
            password="your_password",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

    def init_tables(self):
        try:
            # 创建用户表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    balance INTEGER NOT NULL,
                    token TEXT,
                    terminal TEXT
                )
            """)
            
            # 创建商店表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS stores (
                    store_id TEXT PRIMARY KEY,
                    user_id TEXT REFERENCES users(user_id)
                )
            """)
            
            # 创建订单表
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    user_id TEXT REFERENCES users(user_id),
                    store_id TEXT REFERENCES stores(store_id),
                    status TEXT NOT NULL,
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"初始化表失败: {str(e)}")
