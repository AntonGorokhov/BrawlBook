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
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    rating = db.Column(db.Float, default=1400.0)
    rating_history = db.relationship('Rating_history')
    posts = db.relationship('Post')
    mode = db.Column(db.Integer, default=3)
    k = db.Column(db.Float, default=40.0)
    numrounds = db.Column(db.Integer, default=0)

    def commit_rating_change(self, Dr, round_id):
        self.rating += Dr * self.k
        new_rating_history = Rating_history(value=self.rating, user_id=self.id, round_id=round_id)
        db.session.add(new_rating_history)
        if self.numrounds < 10:
            self.k = 40.0
        else:
            if self.rating >= 2000.0:
                self.k = 10.0
            else:
                self.k = 20.0
        self.numrounds += 1
        db.session.commit()
        return


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_name = db.Column(db.String(20), nullable=False)


class Rating_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    round_id = db.Column(db.Integer, default=-1)


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p11 = db.Column(db.Integer)
    p12 = db.Column(db.Integer)
    p21 = db.Column(db.Integer)
    p22 = db.Column(db.Integer)
    win = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)