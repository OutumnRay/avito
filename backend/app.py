from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from services import send_coins, buy_item
from models import db, User, Product, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/merch_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '3d2f16e84d8e745087c1f6a8ed9142e27b0850984a8d2ac687c90781a04dfe22'

db.init_app(app)
jwt = JWTManager(app)


# Авторизация пользователя
@app.route('/api/auth', methods=['POST'])
def auth():
    from auth import authenticate_user

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Bad username or password"}), 401


# Получение информации о пользователе
@app.route('/api/info', methods=['GET'])
@jwt_required()
def info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    transactions = Transaction.query.filter((Transaction.from_user == user.id) | (Transaction.to_user == user.id)).all()

    received = [{"fromUser": t.from_user, "amount": t.amount} for t in transactions if t.to_user == user.id]
    sent = [{"toUser": t.to_user, "amount": t.amount} for t in transactions if t.from_user == user.id]

    inventory = [{"type": p.name, "quantity": 1} for p in Product.query.all()]

    return jsonify({
        "coins": user.coins,
        "inventory": inventory,
        "coinHistory": {"received": received, "sent": sent}
    })


# Отправка монет другому пользователю
@app.route('/api/sendCoin', methods=['POST'])
@jwt_required()
def send_coin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    to_user = request.json['toUser']
    amount = request.json['amount']

    from services import send_coins
    response = send_coins(user, to_user, amount)
    return response


# Покупка товара
@app.route('/api/buy/<item>', methods=['GET'])
@jwt_required()
def buy(item):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    from services import buy_item
    response = buy_item(user, item)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
