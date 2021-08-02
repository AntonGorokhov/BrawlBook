from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    rating = db.Column(db.Integer, default=1400)

    def __repr__(self):
        return 'User <%r>' % self.id


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return 'Article <%r>' % self.id
