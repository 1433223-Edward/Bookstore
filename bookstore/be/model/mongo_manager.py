import logging
from typing import Dict, Any, Optional
from bson.binary import Binary

class MongoManager:
    def __init__(self, db):
        self.db = db

    def store_book_details(self, book_id: str, details: Dict[str, Any]) -> bool:
        """存储图书详细信息"""
        try:
            self.db.book_details.update_one(
                {"book_id": book_id},
                {"$set": details},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"存储图书详细信息失败: {str(e)}")
            return False

    def store_book_image(self, book_id: str, image_data: bytes) -> bool:
        """存储图书图片"""
        try:
            self.db.book_images.update_one(
                {"book_id": book_id},
                {"$set": {"image": Binary(image_data)}},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"存储图书图片失败: {str(e)}")
            return False

    def get_book_details(self, book_id: str) -> Optional[Dict[str, Any]]:
        """获取图书详细信息"""
        try:
            return self.db.book_details.find_one(
                {"book_id": book_id},
                {"_id": 0}
            )
        except Exception as e:
            logging.error(f"获取图书详细信息失败: {str(e)}")
            return None

    def get_book_image(self, book_id: str) -> Optional[bytes]:
        """获取图书图片"""
        try:
            result = self.db.book_images.find_one({"book_id": book_id})
            return result["image"] if result else None
        except Exception as e:
            logging.error(f"获取图书图片失败: {str(e)}")
            return None

    def store_user_details(self, user_id: str, details: Dict[str, Any]) -> bool:
        """存储用户详细信息"""
        try:
            self.db.user_details.update_one(
                {"user_id": user_id},
                {"$set": details},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"存储用户详细信息失败: {str(e)}")
            return False

    def store_store_details(self, store_id: str, details: Dict[str, Any]) -> bool:
        """存储商店详细信息"""
        try:
            self.db.store_details.update_one(
                {"store_id": store_id},
                {"$set": details},
                upsert=True
            )
            return True
        except Exception as e:
            logging.error(f"存储商店详细信息失败: {str(e)}")
            return False