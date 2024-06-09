from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(50), default='user')  # Add this line

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True)
    author = db.Column(db.String(150))
    file_path = db.Column(db.String(150))  # This will be the path to the digital copy


