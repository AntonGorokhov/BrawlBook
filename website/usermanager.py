from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Post, Rating_history, Round
from flask_login import login_user, logout_user, login_required, current_user
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

usermanager = Blueprint('usermanager', __name__)


xmode = ['Админ++', 'Админ', 'Модератор', 'Простой смертный']


@usermanager.route('/users')
@login_required
def show_all_users():
    all_users = User.query.order_by(User.rating.desc()).all()
    return render_template('all_users.html', all_users=all_users, user=current_user, sz=len(all_users), xmode=xmode)


@usermanager.route('/godmode', methods=['GET', 'POST'])
@login_required
def godmode():
    if request.method == 'POST':
        godmode_activation_code = request.form['godmode_activation_code']
        if check_password_hash(generate_password_hash('123'), godmode_activation_code):
            if User.query.filter_by(mode=0).first():
                flash("Отсоси, мамкин хакер. Хуй тебе, а не режим Бога", category='error')
            else:
                user = User.query.get(current_user.id)
                user.mode = 0
                db.session.commit()
                flash("Вы включили режим Бога! Обоссытесь от счастья!", category='success')
                return redirect(url_for('views.home'))
        else:
            flash("Отсоси, мамкин хакер. Хуй тебе, а не режим Бога", category='error')
            return redirect(url_for('views.home'))
    return render_template('godmode.html', user=current_user)


@usermanager.route('/plot')
def plot():
    x = [1, 2, 3, 4, 5]
    # heights of bars
    y = [10, 24, 36, 40, 5]
    # labels for bars
    tick_label = ['one', 'two', 'three', 'four', 'five']
    # plotting a bar chart
    plt.plot(x, y)

    # naming the y-axis
    plt.ylabel('Рейтинг')
    # naming the x-axis
    plt.xlabel('Время')
    # plot title
    plt.title('Изменение ебучего рейтинга')

    file = open('website/static/images/plot.png', 'wb')
    file.truncate(0)

    plt.savefig(file)

    file.close()
    # plt.show()

    return render_template('plot.html', url='/static/images/plot.png', user=current_user)


@usermanager.route('/user/<int:id>/profile')
@login_required
def user_detail(id):
    round_history = []
    for i in User.query.get(id).rating_history:
        round_history.append(Round.query.get(i.round_id))

    x = []
    y = []
    for i in User.query.get(id).rating_history:
        x.append(i.date + timedelta(minutes=180))
        y.append(i.value)

    # labels for bars
    # plotting a bar chart
    plt.plot(x, y, 'bo', linestyle='dashed')

    # plt.xticks(x[::5])
    plt.ylabel('Рейтинг')
    plt.xlabel('Время')
    plt.title('Изменение ебучего рейтинга')


    # os.remove('website/static/images/plot%s.png' % str(id))
    file = open('website/static/images/plot%s.png' % str(id), 'w').close()
    file = open('website/static/images/plot%s.png' % str(id), 'wb')

    plt.savefig(file)

    file.seek(0)

    file.close()

    plt.close()

    return render_template('profile.html', urlik='/static/images/plot%s.png' % str(id),
                           user=current_user,
                           profile=User.query.get(id),
                           rating_history=User.query.get(id).rating_history,
                           xmode=xmode, round_history=round_history, sz=len(round_history),
                           )


@usermanager.route('/user/<int:id>/update', methods=['POST', 'GET'])
@login_required
def user_update(id):
    if current_user.mode > User.query.get(id).mode or current_user.mode > 1:
        return redirect(url_for('usermanager.show_all_users'))
    if request.method == 'POST':
        user = User.query.get(id)
        name = request.form['name']
        rating = user.rating
        mode = int(user.mode)
        if current_user.mode <= mode:
            rating = float(request.form['rating'])
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
            rating_history = Rating_history(value=rating, user_id=user.id)
            db.session.add(rating_history)
            db.session.commit()
            return redirect('/users')

    return render_template('user_update.html', user=current_user, usr=User.query.get(id))


@usermanager.route('/user/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def user_delete(id):
    if current_user.mode > 1:
        return redirect('/')
    user = User.query.get(id)
    if user.mode <= current_user.mode:
        flash("У тебя еще удалялка не отросла таких людей удалять!", category='error')
        return redirect('/')
    else:
        db.session.delete(user)
        db.commit()
        flash("Ну все. Был пацан, и нет пацана! Помянем!", category='success')
        return redirect('/')