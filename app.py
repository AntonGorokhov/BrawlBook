from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return 'Article <%r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    psw = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return 'User <%r>' % self.id


@app.route("/")
def first_page():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles, sz=len(articles))


@app.route("/posts/<int:id>")
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route("/posts/<int:id>/update", methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        try:
            article.title = request.form['title']
            article.text = request.form['text']
            db.session.commit()
            return redirect('/posts')
        except:
            return "При обновлении ссанины произошла ошибка!"

    if request.method == "GET":
        article = Article.query.get(id)
        return render_template("post_update.html", article=article)


@app.route("/posts/<int:id>/delete")
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "Какое нахуй удаление?"


@app.route("/create_post", methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        article = Article(title=title, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении ссанины произошла ошибка!"

    if request.method == "GET":
        return render_template("create_post.html")


if __name__ == "__main__":
    app.run(debug=True)