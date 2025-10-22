import bcrypt
from app import app, db
from flask import render_template, request, redirect, url_for
from app.models import User, Comment
from app.forms import CreateUserForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user




@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/createuser", methods=["GET", "POST"])
def createuser():
    form = CreateUserForm()
    if form.validate_on_submit():
        bcrypt = Bcrypt()
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("comment"))
    else:
        print("Erro no form")
    return render_template("create_user.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        bcrypt = Bcrypt()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("comment"))
    return render_template("login.html", form=form)

@app.route("/comment", methods=["GET", "POST"])
@login_required
def comment():
    if request.method == "POST":
        new_comment = Comment(content=request.form["comment"], user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        comentarios = Comment.query.all()
        return render_template("comment.html", comentarios=comentarios)
    return render_template("comment.html")