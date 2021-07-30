from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.dp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
blog = SQLAlchemy(app)


class Article(blog.Model):
    id = blog.Column(blog.Integer, primary_key=True)
    title = blog.Column(blog.String(200), nullable=False)
    text = blog.Column(blog.Text, nullable=False)
    date = blog.Column(blog.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Article <%r>' % self.id


@app.route("/")
def first_page():
    return render_template("index.html")

@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route("/posts/<int:id>")
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)



@app.route("/create_post", methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        article = Article(title=title, text=text)
        try:
            blog.session.add(article)
            blog.session.commit()
            return redirect('/')
        except:
            return "При добавлении ссанины произошла ошибка!"

    if request.method == "GET":
        return render_template("create_post.html")


if __name__ == "__main__":
    app.run(debug=True)