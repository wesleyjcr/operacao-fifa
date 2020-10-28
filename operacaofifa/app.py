import os
from dotenv import load_dotenv
from flask import Flask
from operacaofifa.ext import database
from operacaofifa.ext import database_mongo
from operacaofifa.blueprints import bpbot


def create_app():
    app = Flask(__name__)
    load_dotenv('.env')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../storage.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    database.init_app(app)
    database_mongo.init_app(app)
    bpbot.init_app(app)

    return app
