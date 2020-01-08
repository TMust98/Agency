# -*- coding: utf-8 -*-
from app import app, conn
from flask_login import LoginManager, UserMixin


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."


class User(UserMixin):
    def __init__(self, id, login, passwordHash, name, email, phone, servicePrice, idTypeAccountOne, idTypeAccountTwo, idFirm):
        self.id = id
        self.login = login
        self.passwordHash = passwordHash
        self.name = name
        self.email = email
        self.phone = phone
        self.servicePrice = servicePrice
        self.idTypeAccountOne = idTypeAccountOne
        self.idTypeAccountTwo = idTypeAccountTwo
        self.idFirm = idFirm

    def __repr__(self):
        return '<User {}>'.format(self.login)


@login_manager.user_loader
def load_user(user_id):
    cursor = conn.cursor()
    cursor.execute("select * from account where id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9])
    else:
        return None
