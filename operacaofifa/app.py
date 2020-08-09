import telegram
import requests
import locale
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify
from credentials import bot_token, bot_user_name, URL
from sqlalchemy import create_engine

global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

engine = create_engine('sqlite:///storage.db', echo=False)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def update_data():
    req = requests.get(
        'https://meepserver.azurewebsites.net/api/Donate/Payments/F3289933-DB0A-45D7-A23A-E584191B2915')
    data = req.json()

    data_req = {"date_last_request": [datetime.now()]}

    date_request = pd.DataFrame.from_dict(data_req)
    donations = pd.DataFrame(data['donations'])
    quantities = pd.DataFrame(data['quantities'])

    date_request.to_sql('date_last_request', con=engine, if_exists='replace')
    donations.to_sql('donations', con=engine, if_exists='replace')
    quantities.to_sql('quantities', con=engine, if_exists='replace')


def need_to_update():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                'select date_last_request from date_last_request')
            for row in result:
                last_update = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')

                time_delta = datetime.now()-last_update
                minutes_last_update = int(time_delta.total_seconds()/60)

        if minutes_last_update > 60:
            return True
        else:
            return False
    except:
        return True


@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    text = update.message.text.encode("utf-8").decode()

    if text == "/start":
        bot_welcome = """
        Seja bem vindo ao bot da operação fifa, saiba tudo sobre as doações.
        """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)

    elif text == "/status":
        if need_to_update():
            update_data()

        with engine.connect() as connection:
            result = connection.execute(
                'select sum(amount) amount, sum(quantity) quantity from donations')
            for row in result:
                amount = row[0]
                quantity = locale.currency(float(row[1]), grouping=True)

        message = f'''
😀 Veja aqui os dados solicitados:\n
💵 {amount} foram doados até o momento.
📉 Ao todo foram {quantity} doações.

Este bot não tem ligação direta com a Meep, ou o Cruzeiro.\n
É feito de Cruzeirenses para Cruzeirenses, doe e ajude o Cruzeiro.\n
Saiba mais em: https://www.meepdonate.com/live/operacaofifa
        '''
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)
    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(
                text.strip())
            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            bot.sendPhoto(chat_id=chat_id, photo=url,
                          reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            bot.sendMessage(
                chat_id=chat_id,
                text="There was a problem in the name you used, please enter different name",
                reply_to_message_id=msg_id,
            )

    return "ok"


@app.route("/setwebhook", methods=["GET", "POST"])
def set_webhook():
    s = bot.setWebhook("{URL}{HOOK}".format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route("/")
def index():
    return "."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
