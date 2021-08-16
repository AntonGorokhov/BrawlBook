from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Post, Round

views = Blueprint('views', __name__)

xmode = ['Админ++', 'Админ', 'Модератор', 'Простой смертный']


@views.route("/")
def home():
    return render_template("home.html", user=current_user)


@views.route("/about")
def about():
    return render_template("about.html", user=current_user)


@views.route("/terms")
def terms():
    return render_template("terms.html", user=current_user)



