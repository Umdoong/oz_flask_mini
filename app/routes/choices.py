from flask import request, jsonify, Blueprint

from app.models import Choices
from config import db

choices_blp = Blueprint("choices", __name__)

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

def get_choices_by_question_id(question_id):
    choices = (
        Choices.query.filter_by(question_id=question_id, is_active=True).order_by(Choices.sqe).all()
    )
    return choices

@choices_blp.route("/choice/<int:question_id>", methods=["GET", "POST"])
def get_choice_list(question_id):
    choice_list = get_choices_by_question_id(question_id)
    return jsonify({"choices": [choice.to_dict() for choice in choice_list]})

@choices_blp.route("/choice", methods=["GET", "POST"])
def create_choice():
    if request.method == "POST":
        try:
            choice = create_choice()
            return (
                jsonify(
                    {"message": f"Content: {choice.content} choice Success Create"}
                ),
                201,
            )

        except ValueError:
            return jsonify({"message": "error"}), 400