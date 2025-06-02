from flask import jsonify, request, Blueprint

from app.models import Image
from config import db

images_blp = Blueprint("images", __name__)

def create_image():
    data = request.get_json()
    image = Image(
        url=data["url"],
        type=data["type"],
    )
    db.session.add(image)
    db.session.commit()

    return image

def get_all_images():
    images = Image.query.all()
    return [image.to_dict() for image in images]

def get_main_image():
    image = Image.query.filter_by(type="main").first()
    return image

@images_blp.route("/image", methods=["POST"])
def create_image():
    if request.method == "POST":
        try:
            image = create_image()
            return jsonify({"message": f"ID: {image.id} Image Success Create"}), 201

        except ValueError:
            return jsonify({"message": "error"}), 400

@images_blp.route("/image/main", methods=["GET"])
def get_main_image():
    if request.method == "GET":
        image = get_main_image()
        return jsonify({"image": image.url if image.url else None}), 200