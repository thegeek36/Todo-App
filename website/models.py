from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.String(700))
    presentTime=datetime.now()
    date_created = db.Column(db.String,default = presentTime.strftime('%B %d %Y - %I:%M%p'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    todo = db.relationship('Todo')
