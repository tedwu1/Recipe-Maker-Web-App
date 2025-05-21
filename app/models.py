from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

from sqlalchemy.ext.associationproxy import association_proxy

recipe_tags = db.Table(
    'recipe_tags',
    db.Column('recipe_id',  db.Integer, db.ForeignKey('recipe.id'),     primary_key=True),
    db.Column('tag_id',     db.Integer, db.ForeignKey('tag.id'),        primary_key=True)
)

saved_recipes = db.Table(
    'saved_recipes',
    db.Column('user_id',    db.Integer, db.ForeignKey('user.id'),       primary_key=True),
    db.Column('recipe_id',  db.Integer, db.ForeignKey('recipe.id'),     primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True) 
    recipes = db.relationship('Recipe', backref='author', lazy=True)

    saved = db.relationship(
        'Recipe',
        secondary=saved_recipes,
        backref=db.backref('saved_by', lazy='dynamic'),
        lazy='dynamic',
    )

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ratings = db.relationship('Rating', backref='recipe', lazy=True, cascade="all, delete-orphan")

    tags = db.relationship(
        'Tag', 
        secondary='recipe_tags',
        backref=db.backref('recipes', lazy='dynamic'),
        lazy='dynamic', 
    )
    
    def avg_rating(self):
        if not self.ratings:
            return 0
        return round(sum(r.value for r in self.ratings) / len(self.ratings), 1)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)    # Optional review text
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('recipe_id', 'user_id', name='_recipe_user_rating_uc'),)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)