from website import app, db
from flask import render_template, request, redirect
from Non_used.modelsss import User, Article


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
        db.session.rollback()
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
            db.session.rollback()
            return "При добавлении ссанины произошла ошибка!"

    if request.method == "GET":
        return render_template("create_post.html")



@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        name = request.form['name']
        if len(name) == 0:
            return "Конченый ты опущенец, какие тебе катки, если ты даже зарегаться нормально не можешь!"
        psw = request.form['psw']
        user = User(name=name, psw=psw)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return "Конченый ты опущенец, какие тебе катки, если ты даже зарегаться нормально не можешь!"


    if request.method == "GET":
        return render_template("signup.html")


@app.route("/user/<int:id>/profile")
def profile(id):
    user = User.query.get(id)
    return render_template("profile.html", user=user)