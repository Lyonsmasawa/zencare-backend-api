from flask import Flask, jsonify
import os
from src.auth import auth
from src.database import db
from config import config_options
from flask_jwt_extended import JWTManager

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    db.app=app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace('postgres://', 'postgresql://')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app