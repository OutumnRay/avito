from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Модели данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    coins = db.Column(db.Integer, default=1000)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer)
    type = db.Column(db.String(10))  # 'sent' or 'received'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer)
