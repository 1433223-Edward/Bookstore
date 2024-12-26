import pytest
from be.model.store import Store
from be.model.user import User
from be.model.seller import Seller

class TestOrder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.store = Store()
        self.user = User()
        self.seller = Seller()
        
        # 创建测试数据
        self.user.register("test_user", "password")
        self.seller.create_store("test_user", "test_store")
        self.seller.add_book("test_user", "test_store", "test_book", 
                           '{"price": 100}', 10)
        
        yield
        
        # 清理测试数据
        self.user.unregister("test_user", "password")

    def test_new_order(self):
        code, message, order_id = self.store.new_order(
            "test_user", "test_store", [("test_book", 1)])
        assert code == 200
        assert order_id != ""

    def test_payment(self):
        # 先创建订单
        code, message, order_id = self.store.new_order(
            "test_user", "test_store", [("test_book", 1)])
        
        # 充值
        self.user.add_funds("test_user", "password", 1000)
        
        # 支付
        code, message = self.store.payment("test_user", order_id)
        assert code == 200

    def test_ship_order(self):
        # 创建并支付订单
        code, message, order_id = self.store.new_order(
            "test_user", "test_store", [("test_book", 1)])
        self.user.add_funds("test_user", "password", 1000)
        self.store.payment("test_user", order_id)
        
        # 发货
        code, message = self.store.ship_order("test_store", order_id)
        assert code == 200

    def test_receive_order(self):
        # 创建完整订单流程
        code, message, order_id = self.store.new_order(
            "test_user", "test_store", [("test_book", 1)])
        self.user.add_funds("test_user", "password", 1000)
        self.store.payment("test_user", order_id)
        self.store.ship_order("test_store", order_id)
        
        # 收货
        code, message = self.store.receive_order("test_user", order_id)
        assert code == 200 