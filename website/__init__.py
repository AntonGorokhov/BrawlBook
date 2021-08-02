from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "1324354657687980"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///<%s>' % DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    return app


def create_database(app):
    if not path.exists('/website/' + DB_NAME):
        db.create_all(app=app)
        print("Databse Created!")
