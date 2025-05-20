from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, db
from .models import User, Recipe

def get_current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None

# home page
@app.route("/")
def home():
    user = get_current_user()
    return render_template("base.html", user=user)

# authentication
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user     = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for("recipes"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not (username and email and password):
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "warning")
            return render_template("register.html")

        new = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(new)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("home"))


# recipe
@app.route("/recipes")
def recipes():
    user = get_current_user()
    all_recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=all_recipes, user=user)


@app.route("/recipes/add", methods=["GET", "POST"])
def add_recipe():
    user = get_current_user()
    if not user:
        flash("You must be logged in to add a recipe.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        title        = request.form.get("title", "").strip()
        description  = request.form.get("description", "").strip()
        ingredients  = request.form.get("ingredients", "").strip()
        instructions = request.form.get("instructions", "").strip()

        if not (title and description and ingredients and instructions):
            flash("All fields are required.", "danger")
            return render_template("add_recipe.html", user=user)

        new = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            user_id=user.id
        )
        db.session.add(new)
        db.session.commit()
        flash("Recipe added!", "success")
        return redirect(url_for("recipes"))

    return render_template("add_recipe.html", user=user)


@app.route("/recipes/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    user = get_current_user()
    if not user:
        flash("You must be logged in to edit a recipe.", "danger")
        return redirect(url_for("login"))

    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != user.id:
        flash("You can only edit your own recipes.", "danger")
        return redirect(url_for("recipes"))

    if request.method == "POST":
        recipe.title        = request.form.get("title", "").strip()
        recipe.description  = request.form.get("description", "").strip()
        recipe.ingredients  = request.form.get("ingredients", "").strip()
        recipe.instructions = request.form.get("instructions", "").strip()

        if not (recipe.title and recipe.description and recipe.ingredients and recipe.instructions):
            flash("All fields are required.", "danger")
            return render_template("edit_recipe.html", user=user, recipe=recipe)

        db.session.commit()
        flash("Recipe updated!", "success")
        return redirect(url_for("recipes"))

    return render_template("edit_recipe.html", user=user, recipe=recipe)


@app.route("/recipes/delete/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    user = get_current_user()
    recipe = Recipe.query.get_or_404(recipe_id)
    if not user or recipe.user_id != user.id:
        flash("You can only delete your own recipes.", "danger")
        return redirect(url_for("recipes"))

    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe deleted.", "info")
    return redirect(url_for("recipes"))


# 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=get_current_user()), 404
