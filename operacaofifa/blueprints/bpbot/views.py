from flask import jsonify, request
import telegram
from operacaofifa.ext.database import db
from operacaofifa.ext.telegram_bot import bot, TOKEN, URL
from operacaofifa.blueprints.bpbot.controllers import (
    need_to_update,
    update_data,
    view_start,
    view_resume,
    view_last_update,
    view_resume_week,
    register_log,
)
from datetime import datetime


def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    text = update.message.text.encode("utf-8").decode()

    from_message = update.message['from']

    if need_to_update():
        update_data()

    if text == "/start":
        register_log(from_message.username, from_message.first_name,
                     update.message.text, from_message.is_bot)
        message = view_start()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo":
        register_log(from_message.username, from_message.first_name,
                     update.message.text, from_message.is_bot)
        message = view_resume()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/ultima_atualizacao":
        register_log(from_message.username, from_message.first_name,
                     update.message.text, from_message.is_bot)
        message = view_last_update()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo_semanal":
        register_log(from_message.username, from_message.first_name,
                     update.message.text, from_message.is_bot)
        message = view_resume_week()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    return "ok"


def set_webhook():
    s = bot.setWebhook("{URL}{HOOK}".format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


def index():
    return "."


def test():
    if need_to_update():
        update_data()
    with db.engine.connect() as connection:
        result = connection.execute(
            "select sum(amount) amount, sum(quantity) quantity from donations"
        )
        for row in result:
            amount = row[0]
            quantity = row[1]

    return jsonify({"amount": amount, "quantity": quantity})
