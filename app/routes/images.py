from flask import jsonify, request, Blueprint

from app.models import Image
from config import db

images_blp = Blueprint("images", __name__)

def create_image_func():
    data = request.get_json()
    image = Image(
        url=data["url"],
        type=data["type"],
    )
    db.session.add(image)
    db.session.commit()

    return image

@images_blp.route("/image", methods=["POST"])
def create_image():
    if request.method == "POST":
        try:
            image = create_image_func()
            return jsonify({"message": f"ID: {image.id} Image Success Create"}), 201

        except ValueError:
            return jsonify({"message": "error"}), 400

@images_blp.route("/image/main", methods=["GET"])
def get_main_image_route():
    if request.method == "GET":
        image = Image.query.filter_by(type="main").first()
        return jsonify({"image": image.url if image.url else None}), 200