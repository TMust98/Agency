# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField, validators
from wtforms.validators import DataRequired, Email
from app import app, conn
# from flask_login import logout_user, login_required, login_user, current_user
# from app.models import load_user, User


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class CreateAccountForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    passwordOne = PasswordField('Пароль', validators=[DataRequired()])
    passwordTwo = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Создать')


class NewFirmForm(FlaskForm):
    name = StringField('Название фирмы', validators=[DataRequired()])
    inn = IntegerField('ИНН', [validators.DataRequired(), validators.NumberRange(min=100000000000, max=999999999999, message="Введите корректный ИНН : 12 цифр")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Введите корректный email")])
    phone = IntegerField('Номер телефона', [validators.DataRequired(), validators.NumberRange(min=88000000000, max=89999999999, message="Введите корректный номер телефона формата : 89XXXXXXXXX")])
    submit = SubmitField('Добавить')


class ChangeAccountForm(FlaskForm):
    cursor = conn.cursor()
    cursor.execute("select id, title from typeAccountTwo")
    type = cursor.fetchall()
    cursor.close()

    name = StringField('ФИО')
    email = StringField('Email', validators=[Email()])
    phone = IntegerField('Номер телефона', [validators.NumberRange(min=88000000000, max=89999999999, message="Введите корректный номер телефона формата : 89XXXXXXXXX")])
    typeAccountTwo = SelectField('Тип аккаунта', choices=type, coerce=int)
    submit = SubmitField('Сохранить')


class ChangeAccountTypeForm(FlaskForm):
    cursor = conn.cursor()
    cursor.execute("select id, title from typeAccountOne")
    type = cursor.fetchall()
    cursor.close()

    typeAccountOne = SelectField('Род занятий', choices=type, coerce=int)
    submit = SubmitField('Сохранить')


class ChangeAccountPriceForm(FlaskForm):
    servicePrice = IntegerField('Цена за услуги')
    submit = SubmitField('Сохранить')


class ChoiceFirmForm(FlaskForm):
    idFirm = IntegerField('Ид фирмы')
    submit = SubmitField('Выбрать')


class ChoiceShieldForm(FlaskForm):
    idShield = IntegerField('Ид щита')
    submit = SubmitField('Выбрать')


class ChoiceAdvertisementForm(FlaskForm):
    idAdvertisement = IntegerField('Ид объявления')
    submit = SubmitField('Выбрать')


class newContractForm(FlaskForm):
    idAdvertisement = IntegerField('Номер объявления')
    idShield = IntegerField('Номер щита')
    submit = SubmitField('Создать')


class ChangePasswordForm(FlaskForm):
    passwordOld = PasswordField('Старый пароль', validators=[DataRequired()])
    passwordNew1 = PasswordField('Новый пароль', validators=[DataRequired()])
    passwordNew2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Сменить')


class NewAdvertisementForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    image = StringField('URL изображения', validators=[DataRequired()])
    numberDay = IntegerField('Требуемое количество дней', validators=[DataRequired()])
    description = TextAreaField('Описание')
    submit = SubmitField('Создать')


class NewShieldForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    image = StringField('URL изображения')
    address = StringField('Адрес', validators=[DataRequired()])
    price = IntegerField('Цена за день', validators=[DataRequired()])
    description = TextAreaField('Описание')
    submit = SubmitField('Добавить')
