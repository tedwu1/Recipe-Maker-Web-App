from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'

basedir = os.path.abspath(os.path.dirname(__file__))

# using relative pathing here instead
app.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
)

db = SQLAlchemy()
with app.app_context(): 
    db.create_all()
