from flask import Blueprint
from operacaofifa.ext.config import bot_token, bot_user_name, URL
from operacaofifa.blueprints.bpbot.views import index, set_webhook, respond, test, test_data
from operacaofifa.ext.telegram_bot import TOKEN


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
