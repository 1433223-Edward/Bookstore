import pytest
from be.model.mongo_manager import MongoManager
from pymongo import MongoClient

class TestSearch:
    @pytest.fixture(autouse=True)
    def setup(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['bookstore_test']
        self.mongo_manager = MongoManager(db)
        
        # 添加测试数据
        self.mongo_manager.store_book_details("book1", {
            "title": "Python Programming",
            "author": "John Doe",
            "tags": ["programming", "python"],
            "store_id": "store1"
        })
        
        yield
        
        client.drop_database('bookstore_test')

    def test_search_books(self):
        # 测试关键词搜索
        result = self.mongo_manager.search_books("Python")
        assert result is not None
        assert result["total"] == 1
        assert len(result["books"]) == 1
        assert result["books"][0]["title"] == "Python Programming"

    def test_search_with_store(self):
        # 测试店铺内搜索
        result = self.mongo_manager.search_books("Python", store_id="store1")
        assert result is not None
        assert result["total"] == 1
        
        # 测试不存在的店铺
        result = self.mongo_manager.search_books("Python", store_id="non_exist_store")
        assert result is not None
        assert result["total"] == 0 