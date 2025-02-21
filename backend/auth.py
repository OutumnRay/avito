from models import User
from werkzeug.security import check_password_hash

# Функция для аутентификации пользователя
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):  # Предполагается, что в базе есть хеш пароля
        return user
    return None
