from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Post, Rating_history, Round
from flask_login import login_user, logout_user, login_required, current_user


roundmanager = Blueprint('roundmanager', __name__)


xmode = ['Админ++', 'Админ', 'Модератор', 'Простой смертный']


@roundmanager.route('/commit_round', methods=['GET', 'POST'])
@login_required
def add_round():
    if current_user.mode > 1:
        flash("У тебя не достаточно доступа для добавления каточек :(", category='error')
        return redirect('/')
    if request.method == 'POST':
        p11 = request.form['p11']
        p12 = request.form['p12']
        p21 = request.form['p21']
        p22 = request.form['p22']
        if p11 == p12 or p11 == p21 or p11 == p22 or p12 == p21 or p12 == p22 or p21 == p22:
            flash("Конченый ты мудозвон! Имена не могут совпадать!", category='error')
        else:
            user11 = User.query.filter_by(name=p11).first()
            user12 = User.query.filter_by(name=p12).first()
            user21 = User.query.filter_by(name=p21).first()
            user22 = User.query.filter_by(name=p22).first()
            if not user11 or not user22 or not user21 or not user22:
                flash("Блять, ты еблан! Какого-то аккаунта из указанных нет!", category='error')
            else:
                win = float(request.form['win'])
                round = Round(p11=user11.id, p12=user12.id, p21=user21.id, p22=user22.id, win=win)
                db.session.add(round)
                db.session.commit()
                Ra = (user11.rating * user12.rating) ** (0.5)
                Rb = (user21.rating * user22.rating) ** (0.5)
                Ea = 1.0 / (1 + 10 ** ((Rb - Ra) / 400.0))
                Eb = 1.0 / (1 + 10 ** ((Ra - Rb) / 400.0))
                Sa = 1.0
                Sb = 0.0
                if win == 0.0:
                    Sa = 0.0
                    Sb = 1.0
                Da = Sa - Ea
                Db = Sb - Eb
                user11.commit_rating_change(Da, round.id)
                user12.commit_rating_change(Da, round.id)
                user21.commit_rating_change(Db, round.id)
                user22.commit_rating_change(Db, round.id)
                return redirect(url_for('usermanager.show_all_users'))
    return render_template('create_round.html', user=current_user)


@roundmanager.route('rounds/<int:id>')
def round_detail(id):
    return render_template('round_detail.html', user=current_user, round=Round.query.get(id), User=User)