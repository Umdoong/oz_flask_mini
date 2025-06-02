from flask import Flask, jsonify
from flask_migrate import Migrate

import app.models
from app.routes.stats_routes import stats_routes_blp
from app.routes.users import user_blp
from app.routes.questions import questions_blp
from app.routes.images import images_blp
from app.routes.choices import choices_blp
from app.routes.answers import answers_blp
from config import db

migrate = Migrate()


def create_app():
	application = Flask(__name__)

	application.config.from_object("config.Config")
	application.secret_key = "oz_form_secret"

	db.init_app(application)

	migrate.init_app(application, db)

	# 400 에러 발생 시, JSON 형태로 응답 반환
	@application.errorhandler(400)
	def handle_bad_request(error):
		response = jsonify({"message": error.description})
		response.status_code = 400
		return response

	# 블루프린트 등록
	application.register_blueprint(user_blp)
	application.register_blueprint(questions_blp)
	application.register_blueprint(images_blp)
	application.register_blueprint(choices_blp)
	application.register_blueprint(answers_blp)
	application.register_blueprint(stats_routes_blp)


	return application