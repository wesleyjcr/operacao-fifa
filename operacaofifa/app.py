import telegram

from flask import Flask

from blueprints import bpbot


def create_app():
    app = Flask(__name__)
    bpbot.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, threaded=True)
