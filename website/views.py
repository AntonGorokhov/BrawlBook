from flask import Blueprint, render_template, request, redirect
from . import db
from .models import User

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/about")
def about():
    return render_template("about.html")

