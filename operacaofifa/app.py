from flask import Flask
from operacaofifa.ext import database
from operacaofifa.ext import database_mongo
from operacaofifa.blueprints import bpbot


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../storage.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MONGO_URI"] = 'mongodb+srv://telegram_bot:BOToperacaoFIFA2020@cluster0.3pee7.mongodb.net/operacaofifa?retryWrites=true&w=majority'
    database.init_app(app)
    database_mongo.init_app(app)
    bpbot.init_app(app)

    return app
