from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        password2 = request.form['password2']
        if len(name) < 5:
            flash('Ты в край ебнулся? В ссаном имени должно быть не менее 5 символов!', category='error')
        elif len(password) < 5:
            flash('Ты в край ебнулся? В ссаном пароле должно быть не менее 5 символов!', category='error')
        elif User.query.filter_by(name=name).first():
            flash('Ты в край ебнулся? Такой аккаунт уже есть!', category='error')
        elif password2 != password:
            flash('Ты в край ебнулся? Пароли должны совпадать!', category='error')
        else:
            user = User(name=name, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash('Ура! Ссаный аккаунт создан!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html")


@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Ура! Получилось войти!", category='success')
            else:
                flash("Ебучй ты даун! Неправильно введен пароль", category='error')
        else:
            flash("Ебучй ты даун! Такого имени даже нет! Иди нахуй!", category='error')
    return render_template("login.html")

