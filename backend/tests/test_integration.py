import unittest
from models import db, User, Product
from app import app

class TestMerchShopIntegration(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/merch_shop_test'
        self.app = app.test_client()
        db.create_all()

        # Создаем тестовых пользователей и товары
        self.user = User(username='testuser')
        db.session.add(self.user)
        db.session.commit()

        self.product = Product(name="t-shirt", price=80)
        db.session.add(self.product)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_buy_item_integration(self):
        response = self.app.get('/api/buy/t-shirt')
        self.assertEqual(response.status_code, 200)

    def test_send_coins_integration(self):
        response = self.app.post('/api/sendCoin', json={'toUser': 'testuser', 'amount': 100})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
