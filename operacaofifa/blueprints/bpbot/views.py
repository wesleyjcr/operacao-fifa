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
    username = update.message.chat.username
    first_name = update.message.chat.first_name

    if need_to_update():
        update_data()

    if text == "/start":
        register_log(username, first_name,
                     text, False)
        message = view_start()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo":
        register_log(username, first_name,
                     text, False)
        message = view_resume()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/ultima_atualizacao":
        register_log(username, first_name,
                     text, False)
        message = view_last_update()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo_semanal":
        register_log(username, first_name,
                     text, False)
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

    logs = []

    with db.engine.connect() as connection:
        result = connection.execute(
            "select * from logs"
        )
        for row in result:
            logs.append(row[0])

    return jsonify(logs)
