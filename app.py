from flask import Flask, render_template, url_for
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


@app.route("/create_post")
def create_post():
    return render_template("create_post.html")


if __name__ == "__main__":
    app.run(debug=True)