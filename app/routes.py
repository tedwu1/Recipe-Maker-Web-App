from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, db
from .models import User, Recipe, Rating

# helper to get current user
def get_current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None

# Home
@app.route("/")
def home():
    user = get_current_user()
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes, user=user)

# Login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for("recipes"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

# Register
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not (username and email and password):
            flash("All fields are required.", "danger")
            return render_template("register.html")
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash("Username or email already exists.", "warning")
            return render_template("register.html")
        new = User(username=username, email=email,
                   password=generate_password_hash(password))
        db.session.add(new)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("home"))

# List recipes
@app.route("/recipes")
def recipes():
    user = get_current_user()
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        # Search by title or ingredients (case-insensitive)
        all_recipes = Recipe.query.filter(
            (Recipe.title.ilike(f'%{search_query}%')) | 
            (Recipe.ingredients.ilike(f'%{search_query}%'))
        ).all()
    else:
        all_recipes = Recipe.query.all()
    
    return render_template("recipes.html", recipes=all_recipes, user=user)

# Add recipe
@app.route("/recipes/add", methods=["GET","POST"])
def add_recipe():
    user = get_current_user()
    if not user:
        flash("You must be logged in to add a recipe.", "danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title","" ).strip()
        description = request.form.get("description","" ).strip()
        ingredients = request.form.get("ingredients","" ).strip()
        instructions = request.form.get("instructions","" ).strip()
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

# Edit recipe
@app.route('/recipes/edit/<int:recipe_id>', methods=['GET','POST'])
def edit_recipe(recipe_id):
    user = get_current_user(); recipe = Recipe.query.get_or_404(recipe_id)
    if not user:
        flash("Log in to edit recipes.","danger"); return redirect(url_for('login'))
    if recipe.user_id != user.id:
        flash("Only owners can edit.","danger"); return redirect(url_for('recipes'))
    if request.method=='POST':
        recipe.title = request.form.get('title','').strip()
        recipe.description = request.form.get('description','').strip()
        recipe.ingredients = request.form.get('ingredients','').strip()
        recipe.instructions = request.form.get('instructions','').strip()
        if not all([recipe.title,recipe.description,recipe.ingredients,recipe.instructions]):
            flash("All fields required.","danger")
            return render_template('edit_recipe.html',user=user,recipe=recipe)
        db.session.commit(); flash("Recipe updated!","success")
        return redirect(url_for('recipes'))
    return render_template('edit_recipe.html',user=user,recipe=recipe)

# Delete recipe
@app.route('/recipes/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    user = get_current_user(); recipe = Recipe.query.get_or_404(recipe_id)
    if not user or recipe.user_id != user.id:
        flash("Only owners can delete.","danger"); return redirect(url_for('recipes'))
    db.session.delete(recipe); db.session.commit(); flash("Recipe deleted.","info")
    return redirect(url_for('recipes'))

# View recipe (public)
@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    user = get_current_user()
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Get user's existing rating if available
    user_rating = None
    if user:
        user_rating = Rating.query.filter_by(
            recipe_id=recipe_id,
            user_id=user.id
        ).first()
    
    return render_template(
        'view_recipe.html',
        recipe=recipe,
        user=user,
        user_rating=user_rating
    )

# Rate recipe
@app.route('/recipes/<int:recipe_id>/rate', methods=['POST'])
def rate_recipe(recipe_id):
    user = get_current_user()
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if not user:
        flash("Please log in to rate recipes.", "danger")
        return redirect(url_for('login'))
    
    # Get rating value and optional comment from form
    value = int(request.form.get('rating', 0))
    comment = request.form.get('comment', '').strip()
    
    # Validate rating
    if not value or value < 1 or value > 5:
        flash("Please provide a rating between 1 and 5 stars.", "danger")
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    # Check if the user has already rated this recipe
    existing_rating = Rating.query.filter_by(
        recipe_id=recipe_id, 
        user_id=user.id
    ).first()
    
    if existing_rating:
        # Update existing rating
        existing_rating.value = value
        existing_rating.comment = comment
        flash("Your rating has been updated.", "success")
    else:
        # Create new rating
        new_rating = Rating(
            value=value,
            comment=comment,
            recipe_id=recipe_id,
            user_id=user.id
        )
        db.session.add(new_rating)
        flash("Thank you for rating this recipe!", "success")
    
    db.session.commit()
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

# View profile
@app.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        flash("You must be logged in to view your profile.","danger")
        return redirect(url_for('login'))
    my_recipes = Recipe.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, recipes=my_recipes)

# Edit profile
@app.route('/profile/edit', methods=['GET','POST'])
def edit_profile():
    user = get_current_user()
    if not user:
        flash("Log in to edit your profile.","danger")
        return redirect(url_for('login'))
    if request.method=='POST':
        # gather inputs
        new_username = request.form.get('username','').strip()
        new_email = request.form.get('email','').strip()
        new_password = request.form.get('password','').strip()
        # validate
        if not(new_username and new_email):
            flash("Username and email cannot be blank.","danger")
            return render_template('edit_profile.html',user=user)
        # check uniqueness
        if new_email!=user.email and User.query.filter_by(email=new_email).first():
            flash("Email already in use.","warning")
            return render_template('edit_profile.html',user=user)
        # apply updates
        user.username = new_username
        user.email = new_email
        if new_password:
            user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', user=user)

# 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=get_current_user()),404