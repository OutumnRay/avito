from models import db, User, Transaction, Product
from flask import jsonify


# Логика для отправки монет другому пользователю
def send_coins(user, to_user, amount):
    recipient = User.query.filter_by(username=to_user).first()

    if user.coins >= amount:
        user.coins -= amount
        recipient.coins += amount
        db.session.add(Transaction(from_user=user.id, to_user=recipient.id, amount=amount, type='sent'))
        db.session.add(Transaction(from_user=recipient.id, to_user=user.id, amount=amount, type='received'))
        db.session.commit()
        return jsonify({"message": "Coins sent successfully"})
    else:
        return jsonify({"message": "Insufficient coins"}), 400


# Логика для покупки товара
def buy_item(user, item):
    product = Product.query.filter_by(name=item).first()

    if product and user.coins >= product.price:
        user.coins -= product.price
        db.session.add(Transaction(from_user=user.id, to_user=None, amount=product.price, type='sent'))
        db.session.commit()
        return jsonify({"message": f"Purchased {item} successfully"})
    else:
        return jsonify({"message": "Insufficient coins or invalid product"}), 400
