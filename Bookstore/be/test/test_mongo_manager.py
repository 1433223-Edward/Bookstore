import pytest
from be.model.mongo_manager import MongoManager
from pymongo import MongoClient

class TestMongoManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['bookstore_test']
        self.mongo_manager = MongoManager(db)
        yield
        client.drop_database('bookstore_test')

    def test_store_book_content(self):
        book_id = "test_book_1"
        content = "This is a test book content"
        result = self.mongo_manager.store_book_content(book_id, content)
        assert result == True

        # 验证内容是否存储成功
        stored_content = self.mongo_manager.db.book_contents.find_one({"book_id": book_id})
        assert stored_content is not None
        assert stored_content["content"] == content

    def test_store_book_image(self):
        book_id = "test_book_1"
        image_data = b"fake_image_data"
        result = self.mongo_manager.store_book_image(book_id, image_data)
        assert result == True

        # 验证图片是否存储成功
        stored_image = self.mongo_manager.get_book_image(book_id)
        assert stored_image == image_data 