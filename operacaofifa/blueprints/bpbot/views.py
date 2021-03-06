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
    view_week_summary,
    view_month_summary,
    register_log,
    register_feedback
)
from datetime import datetime


def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    text = update.message.text.encode("utf-8").decode()
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    is_bot = update.message.from_user.is_bot

    if need_to_update():
        update_data()

    if text == "/start":
        register_log(username, first_name,
                     text, is_bot)
        message = view_start()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo":
        register_log(username, first_name,
                     text, is_bot)
        message = view_resume()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/ultima_atualizacao":
        register_log(username, first_name,
                     text, is_bot)
        message = view_last_update()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo_semanal":
        register_log(username, first_name,
                     text, is_bot)
        message = view_week_summary()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo_mensal":
        register_log(username, first_name,
                     text, is_bot)
        message = view_month_summary()
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif "/feedback" in text:
        text_clean = text.replace('/feedback', '')
        if text_clean == '' or text_clean == ' ':
            message = 'Ops, seu feedback veio vazio!\n\n'\
                      'Para utilizar este recurso faça o seguinte digite /feedback e uma mensagem \n'\
                      'Por exemplo: \n\n/feedback Gostei do bot dou nota 6 fique feliz é melhor que 1!\n\n'\
                      '🦊 NÓS SOMOS CRUZEIRO 🦊'
            bot.sendMessage(chat_id=chat_id, text=message,
                            reply_to_message_id=msg_id)
        else:
            register_log(username, first_name,
                         text, is_bot)
            message = register_feedback(
                username, first_name, text.replace('/feedback', ''), is_bot)
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
            logs.append({
                "id": row[0],
                "date_time": row[1],
                "username": row[2],
                "first_name": row[3],
                "text": row[4],
                "is_bot": row[5]
            })

    return jsonify(logs)
