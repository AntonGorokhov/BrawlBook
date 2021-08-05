from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime


# USER_MODES
# 0) godmode
# 1) admin
# 2) moderator
# 3) simple-user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    rating = db.Column(db.Float, default=1400.0)
    rating_history = db.relationship('Rating_history')
    posts = db.relationship('Post')
    mode = db.Column(db.Integer, default=3)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_name = db.Column(db.String(20), nullable=False)


class Rating_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
