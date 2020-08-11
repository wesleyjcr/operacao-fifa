import telegram

from flask import Flask

from blueprints import bpbot


app = Flask(__name__)
bpbot.init_app(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
