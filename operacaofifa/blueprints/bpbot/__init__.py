import telegram
from sqlalchemy import create_engine
from operacaofifa.credentials import bot_token, bot_user_name, URL
from operacaofifa.blueprints.bpbot.actions import index, set_webhook, respond, test
from flask import Blueprint


global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

engine = create_engine('sqlite:///storage.db', echo=False)

bp = Blueprint('bpbot', __name__)


def init_app(app):
    app.register_blueprint(bp)


routes = [
    ("/", "index", index, ["GET"]),
    ("/setwebhook", "setwebhook", set_webhook, ["GET", "POST"]),
    (f"/{TOKEN}", "respond", respond, ["POST"]),
    ("/test", "test", test, ['GET'])
]

for route, endpoint, view_func, methods in routes:
    bp.add_url_rule(route, endpoint, view_func, methods=methods)
