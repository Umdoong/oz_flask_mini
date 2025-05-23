from flask import request

from app.models import Question
from config import db


def create_question():
    data = request.get_json()
    question = Question(
        title=data["title"],
        sqe=data["sqe"],
        image_id=data["image_id"],
    )
    db.session.add(question)
    db.session.commit()

    return question


def get_question_by_id(question_id):
    question = Question.query.filter_by(id=question_id, is_active=True).first()
    return question


def get_question_by_sqe(sqe):
    question = Question.query.filter_by(sqe=sqe).first()
    return question


def get_question_sort_by_sqe():
    questions = (
        Question.query.order_by(Question.sqe.desc()).filter_by(is_active=1).all()
    )
    return [question.to_dict() for question in questions]


def get_question_count():
    question = Question.query.filter_by(is_active=True).all()
    count = len(question)
    return count