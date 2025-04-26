# from flask import render_template
# from app import app

# @app.route("/")
# def home():
#     return render_template("base.html")

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template("404.html"), 404

from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models import User

@app.route("/")
def home():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template("base.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session["user_id"] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # Check for existing user
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists. Please try again.", "danger")
            return render_template("register.html")
        # Create and add new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404