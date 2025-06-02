from flask import Blueprint, jsonify, request, flash
from sqlalchemy.exc import IntegrityError

from app.models import User
from config import db

user_blp = Blueprint("users", __name__)

def create_user():
    data = request.get_json()

    user = User(
        name=data["name"], age=data["age"], gender=data["gender"], email=data["email"]
    )

    db.session.add(user)
    db.session.commit()
    return user


@user_blp.route("/", methods=["GET"])
def connect():
    if request.method == "GET":
        return jsonify({"message": "Success Connect"})

@user_blp.route("/signup", methods=["POST"])
def signup_page():
    if request.method == "POST":
        try:
            user = create_user()
            return (
                jsonify(
                    {
                        "message": f"{user.name}님 회원가입을 축하합니다",
                        "user_id": user.id,
                    }
                ),
                201,
            )

        except ValueError or IntegrityError:
            return jsonify({"message": "이미 존재하는 계정 입니다."}), 400