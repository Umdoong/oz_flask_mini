from flask import request

from app.models import Choices
from config import db


def create_choice():
    data = request.get_json()
    choice = Choices(
        content=data["content"],
        sqe=data["sqe"],
        is_active=data["is_active"],
        question_id=data["question_id"],
    )
    db.session.add(choice)
    db.session.commit()

    return choice


def get_choice_by_id(choice_id):
    choice = Choices.query.filter_by(id=choice_id).first()
    return choice


def get_choices_by_question_id(question_id):
    choices = (
        Choices.query.filter_by(question_id=question_id).order_by(Choices.sqe).all()
    )
    return choices