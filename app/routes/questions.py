from flask import request, Blueprint, jsonify

from app.models import Question, Choices
from app.routes.choices import get_choices_by_question_id
from config import db

questions_blp = Blueprint("questions", __name__)

def get_question_by_id(question_id):
    question = Question.query.filter_by(id=question_id, is_active=True).first()
    return question

def get_question_count():
    question = Question.query.filter_by(is_active=True).all()
    count = len(question)
    return count

@questions_blp.route("/question", methods=["POST"])
def create_questions():
    """
    question 생성 API
    """
    if request.method == "POST":
        try:
            data = request.get_json()
            question = Question(
                title=data["title"],
                sqe=data["sqe"],
                image_id=data["image_id"],
            )
            db.session.add(question)
            db.session.commit()

            return (
                jsonify(
                    {"message": f"Title: {question.title} question Success Create"}
                ),
                201,
            )

        except ValueError:
            return jsonify({"message": "error"}), 400

@questions_blp.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    """
    특정 질문 ID에 대한 질문과 선택지를 반환하는 API
    """
    question = get_question_by_id(question_id)
    choice_list = get_choices_by_question_id(question_id)
    return jsonify({"question": question.to_dict(), "choices": [choice.to_dict() for choice in choice_list]})

@questions_blp.route("/questions/count", methods=["GET"])
def count_question():
    if request.method == "GET":
        count = get_question_count()
        return jsonify({"total": count})