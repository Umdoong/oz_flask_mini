from flask import request, jsonify, Blueprint

from app.models import Choices
from config import db

choices_blp = Blueprint("choices", __name__)

def get_choices_by_question_sqe(question_sqe):
    choices = (
        Choices.query.filter_by(question_id=question_sqe, is_active=True).order_by(Choices.sqe).all()
    )
    return choices

@choices_blp.route("/choice", methods=["POST"])
def create_choice():
    if request.method == "POST":
        try:
            data = request.get_json()
            choice = Choices(
                content=data["content"],
                sqe=data["sqe"],
                is_active=data.get("is_active", True),
                question_id=data["question_id"],
            )
            db.session.add(choice)
            db.session.commit()

            return (
                jsonify(
                    {"message": f"Content: {choice.content} choice Success Create"}
                ),
                201,
            )

        except KeyError as e:
            return jsonify({"message": f"Missing required field: {str(e)}"}), 400