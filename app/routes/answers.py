from flask import request, Blueprint, jsonify

from app.models import Answer
from config import db

answers_blp = Blueprint("answers", __name__)

@answers_blp.route("/submit", methods=["GET", "POST"])
def submit_answer():
    if request.method == "POST":
        try:
            for data in request.get_json():
                answer = Answer(
                    user_id=int(data["userId"]),
                    choice_id=data["choiceId"],
                )
                db.session.add(answer)
            db.session.commit()
            user_id = int(request.get_json()[0]["userId"])
            return jsonify({"message": f"User: {user_id}'s answers Success Create"}), 201

        except KeyError as e:
            return jsonify({"message": f"Missing required field: {str(e)}"}), 400