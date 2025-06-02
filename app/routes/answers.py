from flask import request, Blueprint, jsonify

from app.models import Answer
from config import db

answers_blp = Blueprint("answers", __name__)

def submit_answer(data):
    answer = Answer(
        user_id=int(data["userId"]),
        choice_id=data["choiceId"],
    )
    db.session.add(answer)
    db.session.commit()

    return answer

@answers_blp.route("/submit", methods=["GET", "POST"])
def submit_answer():
    if request.method == "POST":
        for answer in request.get_json():
            print(answer)
            submit_answer(data=answer)
        user_id = int(request.get_json()[0]["userId"])
        print(user_id)

        return jsonify({"message": f"User: {user_id}'s answers Success Create"}), 201