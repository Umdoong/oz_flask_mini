from flask import request, Blueprint, jsonify

from app.models import Question, Image
from app.routes.choices import get_choices_by_question_sqe
from config import db

questions_blp = Blueprint("questions", __name__)

def get_question_by_sqe(question_sqe):
    question = Question.query.filter_by(sqe=question_sqe, is_active=True).first()
    if not question:
        return jsonify({"error": "존재하지 않는 질문입니다."}), 404
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

            image = Image.query.get(data["image_id"])

            # 이미지가 없으면 404 error
            if not image:
                return jsonify({"message": "Image not found"}), 404

            # 이미지 타입이 sub가 아니면 400 error
            if image.type.value != "sub":
                return jsonify({"message": "Image type must be 'sub'"}), 400

            question = Question(
                title=data["title"],
                sqe=data["sqe"],
                image_id=data["image_id"],
                is_active=data.get("is_active", True),
            )
            db.session.add(question)
            db.session.commit()

            return jsonify({"message": f"Title: {question.title} question Success Create"}), 201

        except KeyError as e:
            return jsonify({"message": f"Missing required field: {str(e)}"}), 400

@questions_blp.route("/questions/<int:question_sqe>", methods=["GET"])
def get_question(question_sqe):
    """
    특정 질문 ID에 대한 질문과 선택지를 반환하는 API
    """
    question = get_question_by_sqe(question_sqe)
    image = Image.query.get(question.image_id)
    choice_list = get_choices_by_question_sqe(question_sqe)
    return jsonify({
        "title": question.title,
        "image": image.url if image else None,
        "choices": [choice.to_dict() for choice in choice_list]
    })

@questions_blp.route("/questions/count", methods=["GET"])
def count_question():
    if request.method == "GET":
        count = get_question_count()
        return jsonify({"total": count})