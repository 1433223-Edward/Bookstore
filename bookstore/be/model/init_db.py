import logging
from be.model import db_conn
from pymongo import MongoClient

class Store:
    def __init__(self):
        self.db_conn = db_conn.DBConn()
        self.mongo_client = None

    def init_tables(self):
        try:
            conn = self.db_conn.get_db_conn()
            cursor = conn.cursor()
            
            # PostgreSQL: 创建用户表 - 存储核心用户数据
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(255) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL,
                    balance NUMERIC(10,2) NOT NULL DEFAULT 0,
                    token VARCHAR(255),
                    terminal VARCHAR(255)
                );
            """)
            
            # PostgreSQL: 创建商店表 - 存储核心商店数据
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stores (
                    store_id VARCHAR(255) PRIMARY KEY,
                    owner_id VARCHAR(255) REFERENCES users(user_id),
                    store_name VARCHAR(255) NOT NULL
                );
            """)
            
            # PostgreSQL: 创建图书基本信息表 - 存储核心图书数据
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    book_id VARCHAR(255) PRIMARY KEY,
                    store_id VARCHAR(255) REFERENCES stores(store_id),
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255),
                    isbn VARCHAR(255),
                    price NUMERIC(10,2) NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0,
                    CONSTRAINT unique_isbn UNIQUE (isbn)
                );
            """)
            
            # PostgreSQL: 创建订单表 - 存储订单核心数据
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255) REFERENCES users(user_id),
                    store_id VARCHAR(255) REFERENCES stores(store_id),
                    total_price NUMERIC(10,2) NOT NULL,
                    order_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(32) NOT NULL
                );
            """)
            
            conn.commit()
            
            # MongoDB: 初始化连接并创建集合
            self.mongo_client = MongoClient('mongodb://localhost:27017/')
            db = self.mongo_client.bookstore
            
            # 创建所需的集合和索引
            # 1. 图书详细信息集合
            book_details = db.book_details
            book_details.create_index("book_id", unique=True)
            
            # 2. 图书图片集合
            book_images = db.book_images
            book_images.create_index("book_id", unique=True)
            
            # 3. 用户详细信息集合（头像等）
            user_details = db.user_details
            user_details.create_index("user_id", unique=True)
            
            # 4. 商店详细信息集合（店铺介绍、图片等）
            store_details = db.store_details
            store_details.create_index("store_id", unique=True)
            
            # 5. 订单详细信息集合
            order_details = db.order_details
            order_details.create_index("order_id", unique=True)
            
            return True
        except Exception as e:
            logging.error(f"初始化数据库失败: {str(e)}")
            return False
        finally:
            if self.db_conn:
                self.db_conn.close_db_conn()

    def get_db_conn(self):
        return self.db_conn.get_db_conn()

    def get_mongo_db(self):
        return self.mongo_client.bookstore if self.mongo_client else None