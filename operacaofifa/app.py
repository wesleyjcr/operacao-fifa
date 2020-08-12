from flask import Flask
from operacaofifa.ext import database
from operacaofifa.blueprints import bpbot


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../storage.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    database.init_app(app)
    bpbot.init_app(app)

    return app
