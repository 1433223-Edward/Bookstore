import psycopg2
from psycopg2 import pool
import logging


class DBConn:
    def __init__(self):
        self.conn = None
        self.pool = None

    def init_db_pool(self):
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host="localhost",
                database="bookstore",
                user="your_username",
                password="your_password"
            )
            return True
        except Exception as e:
            logging.error(f"数据库连接池初始化失败: {str(e)}")
            return False

    def get_db_conn(self):
        try:
            if self.pool:
                self.conn = self.pool.getconn()
                return self.conn
            return None
        except Exception as e:
            logging.error(f"获取数据库连接失败: {str(e)}")
            return None

    def close_db_conn(self):
        try:
            if self.conn:
                self.pool.putconn(self.conn)
                self.conn = None
        except Exception as e:
            logging.error(f"关闭数据库连接失败: {str(e)}")

    def user_id_exist(self, user_id):
        cursor = self.conn.execute(
            "SELECT user_id FROM user WHERE user_id = ?;", (user_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        cursor = self.conn.execute(
            "SELECT book_id FROM store WHERE store_id = ? AND book_id = ?;",
            (store_id, book_id),
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        cursor = self.conn.execute(
            "SELECT store_id FROM user_store WHERE store_id = ?;", (store_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True
