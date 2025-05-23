from flask import Blueprint, jsonify, request, session

from app.models import Choices
from app.services import answers, choices, images, questions, users

routes = Blueprint("routes", __name__)


@routes.route("/", methods=["GET", "POST"])
def connect():
    if request.method == "GET":
        return jsonify({"message": "Success Connect"})

@routes.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        try:
            user = users.create_user()
            return (
                jsonify(
                    {
                        "message": f"{user.name}님 회원가입을 축하합니다",
                        "user_id": user.id,
                    }
                ),
                201,
            )

        except ValueError:
            return jsonify({"message": "이미 존재하는 계정 입니다."}), 400


@routes.route("/question/<int:question_id>", methods=["GET", "POST"])
def question_page(question_id):
    """
    특정 질문 ID에 대한 질문과 선택지를 반환합니다.
    """
    # 질문 데이터 가져오기
    question = questions.get_question_by_id(question_id)
    if not question:
        return jsonify({"error": "질문을 찾을 수 없습니다."}), 404

    # 선택지 데이터 가져오기
    choice_list = (
        Choices.query.filter_by(question_id=question_id, is_active=True)
        .order_by(Choices.sqe.desc())
        .all()
    )
    choice_data = [choice.to_dict() for choice in choice_list]

    # JSON 응답
    return jsonify(
        {
            "id": question.id,
            "title": question.title,
            "image": question.image.url if question.image else None,
            "choices": choice_data,
        }
    )


@routes.route("/questions/<int:question_id>", methods=["GET", "POST"])
def get_question(question_id):
    question = questions.get_question_by_id(question_id)
    choice_list = choices.get_choices_by_question_id(question_id)
    return jsonify({"question": question.to_dict(), "choices": [choice.to_dict() for choice in choice_list]})


@routes.route("/choice/<int:question_id>", methods=["GET", "POST"])
def get_choice_list(question_id):
    choice_list = choices.get_choices_by_question_id(question_id)
    return jsonify({"choices": [choice.to_dict() for choice in choice_list]})


@routes.route("/questions/count", methods=["GET"])
def count_question():
    if request.method == "GET":
        count = questions.get_question_count()
        return jsonify({"total": count})


@routes.route("/submit", methods=["GET", "POST"])
def submit_answer():
    if request.method == "POST":
        for answer in request.get_json():
            print(answer)
            answers.submit_answer(data=answer)
        user_id = int(request.get_json()[0]["userId"])
        print(user_id)

        return jsonify({"message": f"User: {user_id}'s answers Success Create"}), 201


@routes.route("/image", methods=["GET", "POST"])
def create_image():
    if request.method == "POST":
        try:
            image = images.create_image()
            return jsonify({"message": f"ID: {image.id} Image Success Create"}), 201

        except ValueError:
            return jsonify({"message": "error"}), 400


@routes.route("/question", methods=["GET", "POST"])
def create_questions():
    if request.method == "POST":
        try:
            question = questions.create_question()
            return (
                jsonify(
                    {"message": f"Title: {question.title} question Success Create"}
                ),
                201,
            )

        except ValueError:
            return jsonify({"message": "error"}), 400


@routes.route("/choice", methods=["GET", "POST"])
def create_choice():
    if request.method == "POST":
        try:
            choice = choices.create_choice()
            return (
                jsonify(
                    {"message": f"Content: {choice.content} choice Success Create"}
                ),
                201,
            )

        except ValueError:
            return jsonify({"message": "error"}), 400