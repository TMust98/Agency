# -*- coding: utf-8 -*-
from app import app, conn
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, CreateAccountForm, ChangeAccountForm, ChangePasswordForm, NewFirmForm, NewAdvertisementForm, NewShieldForm, ChangeAccountTypeForm, ChangeAccountPriceForm, ChoiceFirmForm, ChoiceShieldForm, ChoiceAdvertisementForm, newContractForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, login_user, current_user
from app.models import load_user, User
from datetime import date, timedelta
import os


cursor = conn.cursor()


@app.route('/')
@app.route('/advertisements')
def advertisements():
    cursor.execute('select id, title, image, numberDay, dateStart, description from advertisement where dateFinish > current_date order by datestart desc, id desc;')
    ads = cursor.fetchall()
    return render_template('advertisements.html', title='Объявления', ads=ads)


@app.route('/myAdvertisements', methods=['GET', 'POST'])
def myAdvertisements():
    cursor.execute('select id, title, image, numberDay, dateStart, dateFinish, description, current_date from advertisement where idAccount = %s;', (current_user.id,))
    ads = cursor.fetchall()
    form = ChoiceAdvertisementForm()
    if form.validate_on_submit():
        cursor.execute('update advertisement set dateStart = %s, dateFinish = %s where id = %s;', (date.today(), date.today() + timedelta(30), form.idAdvertisement.data,))
        conn.commit()
        flash('Ваше объявление авктивированно на 30 дней.')
        return redirect(url_for('advertisements'))
    return render_template('myAdvertisements.html', title='Мои объявления', ads=ads, form=form)


@app.route('/newAdvertisement', methods=['GET', 'POST'])
@login_required
def newAdvertisement():
    if checkDataAccountFull() == 0:
        flash('Вы не заполнили данные профиля')
        return redirect(url_for('fillAccount'))
    if current_user.idTypeAccountOne != 3:
        flash('Вы не рекламодатель')
        return redirect(url_for('account'))
    form = NewAdvertisementForm()
    if form.validate_on_submit():
        cursor.execute('insert into advertisement (title, image, numberDay, dateStart, dateFinish, idAccount, description) values (%s, %s, %s, %s, %s, %s, %s);', (form.title.data, form.image.data, form.numberDay.data, date.today(), date.today() + timedelta(30), current_user.id, form.description.data,))
        conn.commit()
        flash('Ваше объявление добавлено на 30 дней.')
        return redirect(url_for('advertisements'))
    return render_template('newAdvertisement.html', title='Новое объявление', form=form)


@app.route('/shields')
def shields():
    cursor.execute('select id, title, image, address, price, description from shield where freedom = true order by id desc;')
    shields = cursor.fetchall()
    return render_template('shields.html', title='Щиты', shields=shields)


@app.route('/myShields', methods=['GET', 'POST'])
def myShields():
    cursor.execute('select id, title, image, address, price, description, freedom from shield where idAccount = %s;', (current_user.id,))
    shields = cursor.fetchall()
    form = ChoiceShieldForm()
    if form.validate_on_submit():
        cursor.execute('update shield set freedom = true where id = %s;', (form.idShield.data,))
        conn.commit()
        flash('Ваш щит теперь числится свободным.')
        return redirect(url_for('advertisements'))
    return render_template('myShields.html', title='Мои щиты', shields=shields, form=form)


@app.route('/newShield', methods=['GET', 'POST'])
@login_required
def newShield():
    if checkDataAccountFull() == 0:
        flash('Вы не заполнили данные профиля')
        return redirect(url_for('fillAccount'))
    if current_user.idTypeAccountOne != 4:
        flash('Вы не установщик')
        return redirect(url_for('account'))
    form = NewShieldForm()
    if form.validate_on_submit():
        if form.image.data == "":
            form.image.data = 'http://manual-m.ru/wp-content/uploads/2019/10/no-image-300x300.jpeg';
        cursor.execute('insert into shield (title, image, address, price, idAccount, description) values (%s, %s, %s, %s, %s, %s);', (form.title.data, form.image.data, form.address.data, form.price.data, current_user.id, form.description.data,))
        conn.commit()
        flash('Ваш щит добавлен в базу.')
        return redirect(url_for('shields'))
    return render_template('newShield.html', title='Новый щит', form=form)


@app.route('/firms', methods=['GET', 'POST'])
@login_required
def firms():
    cursor.execute('select * from firm where id != 1;')
    firms = cursor.fetchall()
    form = ChoiceFirmForm()
    if form.validate_on_submit():
        cursor.execute('update account set idFirm = %s where id = %s;', (form.idFirm.data, current_user.id,))
        conn.commit()
        login_user(load_user(current_user.id))
        flash('Вы успешно выбрали фирму.')
    return render_template('firms.html', title='Фирмы', firms=firms, form=form)


@app.route('/newFirm', methods=['GET', 'POST'])
@login_required
def newFirm():
    form = NewFirmForm()
    if form.validate_on_submit():
        cursor.execute('select * from firm where inn = %s or email = %s or phone  = %s;', (form.inn.data, form.email.data, form.phone.data,))
        firm = cursor.fetchone()
        if firm:
            flash('Фирма с таким ИНН, email или телефоном уже существует.')
            return redirect(url_for('newFirm'))
        cursor.execute('insert into firm (inn, name, email, phone) values (%s, %s, %s, %s);', (form.inn.data, form.name.data, form.email.data, form.phone.data,))
        conn.commit()
        flash('Фирма добавлена в базу.')
        return redirect(url_for('firms'))
    return render_template('newFirm.html', title='Добавление фирмы', form=form)


@app.route('/advertisementAndShield', methods=['GET', 'POST'])
@login_required
def advertisementAndShield():
    if checkDataAccountFull() == 0:
        flash('Вы не заполнили данные профиля')
        return redirect(url_for('fillAccount'))
    if current_user.idTypeAccountOne != 2:
        flash('Вы не агент')
        return redirect(url_for('account'))
    cursor.execute('select id, title, image, address, price, description from shield where freedom = true order by id desc;')
    shields = cursor.fetchall()
    cursor.execute('select id, title, image, numberDay, dateStart, description from advertisement where dateFinish > current_date order by datestart desc, id desc;')
    ads = cursor.fetchall()
    form = newContractForm()
    if form.validate_on_submit():
        cursor.execute('select id, numberDay from advertisement where id = %s and dateFinish > current_date;', (form.idAdvertisement.data,))
        advertisement = cursor.fetchone()
        if advertisement is None:
            flash('Не существует данного объявления, или оно истекло.')
            return redirect(url_for('advertisementAndShield'))
        cursor.execute('select id, price, idAccount from shield where id = %s and freedom = true;', (form.idShield.data,))
        shield = cursor.fetchone()
        if shield is None:
            flash('Не существует данного щита, или он занят.')
            return redirect(url_for('advertisementAndShield'))
        cursor.execute('update shield set freedom = false where id = %s;', (form.idShield.data,))
        cursor.execute('select servicePrice from account where id = %s;', (shield[2],))
        installationPrice = cursor.fetchone()
        cursor.execute('select servicePrice from account where id = %s;', (current_user.id,))
        agencyPrice = cursor.fetchone()
        textContract = "Договор №"
        cursor.execute('insert into contract (title, dateStart, dateFinish, price, idAccount, idShield, idAdvertisement) values (%s, %s, %s, %s, %s, %s, %s);', (textContract, date.today() + timedelta(1), date.today() + timedelta(1 + advertisement[1]), advertisement[1] * shield[1] + installationPrice[0] + agencyPrice[0], current_user.id, form.idShield.data, form.idAdvertisement.data,))
        cursor.execute('select max(id) from contract;')
        contrsctId = cursor.fetchone()
        cursor.execute('update contract set title = %s where id = %s;', (textContract + str(contrsctId[0]), contrsctId[0],))
        conn.commit()
        flash('Договор оформлен успешно.')
        return redirect(url_for('myContracts'))
    return render_template('advertisementAndShield.html', title='Объявления и щиты', shields=shields, ads=ads, form=form)


@app.route('/myContracts', methods=['GET', 'POST'])
def myContracts():
    cursor.execute('select title, dateStart, dateFinish, price, idShield, idAdvertisement from contract where idAccount = %s;', (current_user.id,))
    contracts = cursor.fetchall()
    return render_template('myContracts.html', title='Мои контракты', contracts=contracts)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.idTypeAccountOne == 1:
        form = ChangeAccountTypeForm()
    else:
        form = ChangeAccountPriceForm()
    if current_user.idFirm != 1 and current_user.idTypeAccountTwo == 2:
        cursor.execute('select * from firm where id = %s;', (current_user.idFirm,))
        firm = cursor.fetchone()
    else:
        firm = None
    if form.validate_on_submit():
        if current_user.idTypeAccountOne == 1:
            cursor.execute('update account set idTypeAccountOne = %s where id = %s;', (form.typeAccountOne.data, current_user.id))
            conn.commit()
            login_user(load_user(current_user.id))
            flash('Тип учетной записи записан.')
            return redirect(url_for('account'))
        else:
            cursor.execute('update account set servicePrice = %s where id = %s;', (form.servicePrice.data, current_user.id))
            conn.commit()
            login_user(load_user(current_user.id))
            flash('Цена за услуги изменена.')
            return redirect(url_for('account'))
    return render_template('account.html', title='Личный кабинет', form=form, firm=firm)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    if current_user.is_authenticated:
        flash('Для регистрации нового аккаунта выйдите из существующего')
        return redirect(url_for('account'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        cursor.execute('select * from account where login = %s;', (form.login.data,))
        user = cursor.fetchone()
        if user:
            flash('Учетная запись с таким логином уже существует!')
            return redirect(url_for('createAccount'))
        if form.passwordOne.data == form.passwordTwo.data:
            cursor.execute('insert into account (login, passwordHash, idTypeAccountOne, idTypeAccountTwo, idFirm) values (%s, %s, 1, 1, 1);', (form.login.data, generate_password_hash(form.passwordOne.data),))
            conn.commit()
            cursor.execute('select id from account where login = %s;', (form.login.data,))
            user = cursor.fetchone()
            login_user(load_user(user[0]), remember=0)
            flash('Учетная запись создана успешно. Заполните данные профиля.')
            return redirect(url_for('fillAccount'))
        else:
            flash('Пароли не совпадают.')
            return redirect(url_for('createAccount'))
    return render_template('createAccount.html', title='Создание аккаунта', form=form)


@app.route('/fillAccount', methods=['GET', 'POST'])
@login_required
def fillAccount():
    form = ChangeAccountForm()
    if form.validate_on_submit():
        cursor.execute('select id from account where email = %s or phone = %s;', (form.email.data, form.phone.data,))
        user = cursor.fetchone()
        if user:
            flash('Учетная запись с таким email или телефоном уже существует!')
            return redirect(url_for('fillAccount'))
        cursor.execute('update account set name = %s, email = %s, phone = %s, idTypeAccountTwo = %s where id = %s;', (form.name.data, form.email.data, form.phone.data, form.typeAccountTwo.data, current_user.id))
        conn.commit()
        login_user(load_user(current_user.id), remember=0)
        flash('Спасибо за заполнение данных.')
        return redirect(url_for('account'))
    return render_template('changeAccount.html', title='Заполнение данных профиля', form=form)


@app.route('/changeAccount', methods=['GET', 'POST'])
@login_required
def changeAccount():
    form = ChangeAccountForm()
    if form.validate_on_submit():
        cursor.execute('select id from account where (email = %s or phone = %s ) and id != %s;', (form.email.data, form.phone.data, current_user.id,))
        user = cursor.fetchone()
        if user:
            flash('Учетная запись с таким email или телефоном уже существует!')
            return redirect(url_for('changeAccount'))
        cursor.execute('update account set name = %s, email = %s, phone = %s, idTypeAccountTwo = %s where id = %s;', (form.name.data, form.email.data, form.phone.data, form.typeAccountTwo.data, current_user.id,))
        conn.commit()
        login_user(load_user(current_user.id))
        flash('Данные изменены.')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        cursor.execute('select name, email, phone, idTypeAccountTwo from account where id = %s;', (current_user.id,))
        user = cursor.fetchone()
        if user[0]:
            form.name.data = user[0]
        if user[1]:
            form.email.data = user[1]
        if user[2]:
            form.phone.data = user[2]
        if user[3]:
            form.typeAccountTwo.data = user[3]
    return render_template('changeAccount.html', title='Изменение данных профиля', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже авторизированны')
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        cursor.execute('select id, passwordHash from account where login = %s;', (form.login.data,))
        user = cursor.fetchone()
        if user is None or not check_password_hash(user[1], form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        login_user(load_user(user[0]), remember=form.remember_me.data)
        flash('Вы успешно авторизировались')
        return redirect(url_for('account'))
    return render_template('login.html', title='Вход', form=form)


@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.passwordHash, form.passwordOld.data) and form.passwordNew1.data == form.passwordNew2.data:
            cursor.execute('update account set passwordHash = %s where id = %s;', (generate_password_hash(form.passwordNew1.data), current_user.id,))
            conn.commit()
            flash('Пароль был успешно изменен')
            return redirect(url_for('account'))
        else:
            flash('Старый пароль введен неверно или новые пароли не совпадают')
            return redirect(url_for('changePassword'))
    return render_template('changePassword.html', title='Смена пароля', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из профиля')
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    conn.rollback()
    return render_template('500.html'), 500


def checkDataAccountFull():
    if current_user.name is None or current_user.email is None or current_user.phone is None or current_user.idTypeAccountTwo is None:
        return 0
    else:
        return 1
