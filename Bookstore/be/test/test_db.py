import pytest
from be.model.db_conn import DBConn

class TestDB:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.db = DBConn()
        yield
        self.db.conn.close()

    def test_connection(self):
        assert self.db.conn is not None
        assert not self.db.conn.closed

    def test_init_tables(self):
        self.db.init_tables()
        # 验证表是否创建成功
        self.db.cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = self.db.cursor.fetchall()
        table_names = [table[0] for table in tables]
        assert 'users' in table_names
        assert 'stores' in table_names
        assert 'orders' in table_names 