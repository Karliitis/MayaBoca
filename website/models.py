from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    tasks = db.relationship("Task")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    questions = db.relationship("Question")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150))
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    answers = db.relationship("Answer")


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
