from flask import request

from app.models import Answer
from config import db


def create_answer(data):
    answer = Answer(
        user_id=data["user_id"],
        choice_id=data["choice_id"],
    )
    db.session.add(answer)
    db.session.commit()

    return answer


def submit_answer(data):
    answer = Answer(
        user_id=int(data["userId"]),
        choice_id=data["choiceId"],
    )
    db.session.add(answer)
    db.session.commit()

    return answer
