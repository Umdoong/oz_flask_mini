from flask import jsonify, request

from app.models import Image
from config import db


def create_image():
    data = request.get_json()
    image = Image(
        url=data["url"],
        type=data["type"],
    )
    db.session.add(image)
    db.session.commit()

    return image


def get_images_by_id(image_id):
    image = Image.query.filter_by(id=image_id).first()
    return image.to_dict()


def get_images_by_type(image_type):
    images = Image.query.filter_by(type=image_type).all()
    return [image.to_dict() for image in images]


def get_all_images():
    images = Image.query.all()
    return [image.to_dict() for image in images]


def get_main_image():
    image = Image.query.filter_by(type="main").first()
    return image