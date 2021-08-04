from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Post
from flask_login import login_user, logout_user, login_required, current_user

usermanager = Blueprint('usermanager', __name__)


@usermanager.route('/users')
@login_required
def show_all_users():
    all_users = User.query.order_by(User.rating.desc()).all()
    return render_template('all_users.html', all_users=all_users, user=current_user, sz=len(all_users))


@usermanager.route('/godmode', methods=['GET', 'POST'])
@login_required
def godmode():
    if request.method == 'POST':
        godmode_activation_code = request.form['godmode_activation_code']
        if check_password_hash(generate_password_hash('123'), godmode_activation_code):
            user = User.query.get(current_user.id)
            user.mode = 0
            db.session.commit()
            flash("Вы включили режим Бога. Поините! С большой силой приходит большая ответсвенность!", category='success')
            return redirect(url_for('views.home'))
        else:
            flash("Вы включили режим Бога! Обоссытесь от счастья!", category='success')
            return redirect(url_for('views.home'))
    return render_template('godmode.html')


@usermanager.route('/user/<int:id>/profile')
@login_required
def user_detail(id):
    return render_template('profile.html', user=current_user, profile=User.query.get(id))


@usermanager.route('/user/<int:id>/update', methods=['POST', 'GET'])
@login_required
def user_update(id):
    if current_user.mode > User.query.get(id).mode or current_user.mode > 1:
        return redirect(url_for('usermanager.show_all_users'))
    if request.method == 'POST':
        user = User.query.get(id)
        name = request.form['name']
        rating = int(request.form['rating'])
        mode = int(user.mode)
        if current_user.mode <= mode:
            mode = int(request.form['mode'])
        if name != user.name and User.query.filter_by(name=name).first():
            flash('Такое Имя уже существует! Надо как-то покреативничать!', category='error')
        elif rating < 0 or rating > 10000:
            flash('Ты что ебнулся? Ты нормальный рейтинг-то выбери, а?', category='error')
        elif user.id != current_user.id and mode <= current_user.mode:
            flash('Ты не можешь выдать уровень доступа пизже или равный твоему', category='error')
        elif mode > 3:
            flash('Ты не можешь сделать уровень юзера меньше 3. Самые бомжи имеют доступ 3', category='error')
        elif user.id == current_user.id and mode > current_user.mode:
            flash('Ты с дуба рухнул? Нахуй тебе свой же уровень доступа ухудшать?!', category='error')
        else:
            user.name = name
            user.rating = rating
            user.mode = mode
            db.session.commit()

    return render_template('user_update.html', user=current_user, usr=User.query.get(id))