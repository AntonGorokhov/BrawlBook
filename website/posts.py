from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Post
from flask_login import login_user, logout_user, login_required, current_user

posts = Blueprint('posts', __name__)


@posts.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        if len(title) == 0 or len(text) == 0:
            flash('Ебучий ты даун! Надо что-то написать, чтобы это отправилось!', category='error')
        else:
            post = Post(title=title, text=text, user_id=current_user.id, author_name=current_user.name)
            db.session.add(post)
            db.session.commit()
            flash('Молодец, нассал! Теперь все увидят, как ты обоссался!', category='success')
    return render_template('create_post.html', user=current_user)


@posts.route('/posts')
@login_required
def all_posts():
    articles = Post.query.order_by(Post.date.desc()).all()
    return render_template('posts.html', user=current_user,
                           articles=articles,
                           sz=len(articles))


@posts.route('/post/<int:id>')
@login_required
def post_detail(id):
    post = Post.query.get(id)
    return render_template('post_detail.html', article=post, user=current_user)
