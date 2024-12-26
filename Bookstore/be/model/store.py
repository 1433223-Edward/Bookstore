import logging
import os
import sqlite3 as sqlite
import threading
import time


class Store:
    database: str

    def __init__(self, db_path):
        self.database = os.path.join(db_path, "be.db")
        self.init_tables()

    def init_tables(self):
        try:
            conn = self.get_db_conn()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS user ("
                "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
                "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id TEXT, store_id, PRIMARY KEY(user_id, store_id));"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
                " PRIMARY KEY(store_id, book_id))"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order( "
                "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
                "PRIMARY KEY(order_id, book_id))"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS order_status ("
                "order_id TEXT PRIMARY KEY,"
                "status TEXT NOT NULL,"  # pending, paid, shipped, received, cancelled
                "create_time INTEGER NOT NULL,"
                "pay_time INTEGER,"
                "ship_time INTEGER,"
                "receive_time INTEGER,"
                "cancel_time INTEGER)"
            )

            conn.commit()
        except sqlite.Error as e:
            logging.error(e)
            conn.rollback()

    def get_db_conn(self) -> sqlite.Connection:
        return sqlite.connect(self.database)

    def ship_order(self):
        # 发货功能
        pass
        
    def receive_order(self):
        # 收货功能
        pass

    def new_order(self, user_id: str, store_id: str, books: []) -> (int, str, str):
        order_id = ""
        try:
            # 检查库存
            for book_id, count in books:
                cursor = self.conn.execute(
                    "SELECT stock_level FROM store WHERE store_id = ? AND book_id = ?",
                    (store_id, book_id))
                row = cursor.fetchone()
                if row is None or row[0] < count:
                    return error.error_stock_level_low(book_id)

            # 创建订单
            order_id = "{}_{}_{}".format(user_id, store_id, str(time.time()))
            self.conn.execute(
                "INSERT INTO new_order (order_id, user_id, store_id, status) VALUES (?, ?, ?, ?)",
                (order_id, user_id, store_id, "pending"))

            # 添加订单详情
            for book_id, count in books:
                self.conn.execute(
                    "INSERT INTO new_order_detail (order_id, book_id, count) VALUES (?, ?, ?)",
                    (order_id, book_id, count))

            self.conn.commit()
            return 200, "ok", order_id
        except sqlite.Error as e:
            return 528, "{}".format(str(e)), ""

    def payment(self, user_id: str, order_id: str) -> (int, str):
        try:
            # 检查订单状态
            cursor = self.conn.execute(
                "SELECT status, store_id FROM new_order WHERE order_id = ?", (order_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)
            if row[0] != "pending":
                return error.error_invalid_order_status()

            # 计算总价
            cursor = self.conn.execute(
                "SELECT SUM(price * count) FROM new_order_detail WHERE order_id = ?",
                (order_id,))
            total_price = cursor.fetchone()[0]

            # 扣款
            cursor = self.conn.execute(
                "UPDATE user SET balance = balance - ? WHERE user_id = ? AND balance >= ?",
                (total_price, user_id, total_price))
            if cursor.rowcount == 0:
                return error.error_not_sufficient_funds(order_id)

            # 更新订单状态
            self.conn.execute(
                "UPDATE new_order SET status = ? WHERE order_id = ?",
                ("paid", order_id))

            self.conn.commit()
            return 200, "ok"
        except sqlite.Error as e:
            return 528, "{}".format(str(e))

    def ship_order(self, store_id: str, order_id: str) -> (int, str):
        try:
            # 检查订单状态
            cursor = self.conn.execute(
                "SELECT status FROM new_order WHERE order_id = ? AND store_id = ?",
                (order_id, store_id))
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)
            if row[0] != "paid":
                return error.error_invalid_order_status()

            # 更新订单状态
            self.conn.execute(
                "UPDATE new_order SET status = ? WHERE order_id = ?",
                ("shipped", order_id))

            self.conn.commit()
            return 200, "ok"
        except sqlite.Error as e:
            return 528, "{}".format(str(e))

    def receive_order(self, user_id: str, order_id: str) -> (int, str):
        try:
            # 检查订单状态
            cursor = self.conn.execute(
                "SELECT status FROM new_order WHERE order_id = ? AND user_id = ?",
                (order_id, user_id))
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)
            if row[0] != "shipped":
                return error.error_invalid_order_status()

            # 更新订单状态
            self.conn.execute(
                "UPDATE new_order SET status = ? WHERE order_id = ?",
                ("received", order_id))

            self.conn.commit()
            return 200, "ok"
        except sqlite.Error as e:
            return 528, "{}".format(str(e))

    def auto_cancel_order(self):
        try:
            current_time = int(time.time())
            timeout = 30 * 60  # 30分钟超时

            # 查找超时未支付的订单
            cursor = self.conn.execute(
                "SELECT order_id FROM new_order "
                "WHERE status = 'pending' AND create_time < ?",
                (current_time - timeout,)
            )
            
            # 取消超时订单
            for row in cursor:
                order_id = row[0]
                self.conn.execute(
                    "UPDATE new_order SET status = 'cancelled' "
                    "WHERE order_id = ?", (order_id,)
                )
                self.conn.execute(
                    "UPDATE order_status SET "
                    "status = 'cancelled', cancel_time = ? "
                    "WHERE order_id = ?",
                    (current_time, order_id)
                )

            self.conn.commit()
        except sqlite.Error as e:
            logging.error(f"自动取消订单失败: {str(e)}")


database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()


def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
