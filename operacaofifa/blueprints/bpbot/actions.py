from flask import jsonify, request
import pandas as pd
import requests
import locale
from datetime import datetime
from operacaofifa.ext.database import db
from operacaofifa.ext.telegram_bot import bot, TOKEN, URL


def update_data():
    req = requests.get(
        'https://meepserver.azurewebsites.net/api/Donate/Payments/F3289933-DB0A-45D7-A23A-E584191B2915')
    data = req.json()

    data_req = {"date_last_request": [datetime.now()]}

    date_request = pd.DataFrame.from_dict(data_req)
    donations = pd.DataFrame(data['donations'])
    quantities = pd.DataFrame(data['quantities'])

    date_request.to_sql('date_last_request',
                        con=db.engine, if_exists='replace')
    donations.to_sql('donations', con=db.engine, if_exists='replace')
    quantities.to_sql('quantities', con=db.engine, if_exists='replace')


def need_to_update():
    try:
        with db.engine.connect() as connection:
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


def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    text = update.message.text.encode("utf-8").decode()

    if need_to_update():
        update_data()

    if text == "/start":
        message = 'Olá seja bem vindo ao Bot da Operação FIFA\n\n'\
            'Este bot é uma iniciativa de torcedores e não possui vínculo '\
            'com a Meep e nem com o Cruzeiro.\n'\
            'Uma solução de torcedores para torcedores em nome da transparência!\n\n'\
            '🦊 NÓS SOMOS CRUZEIRO 🦊\n\n'\
            'Você pode interagir com o bot com os seguintes comandos:\n'\
            '/start - Iniciar o bot\n\n'\
            '/resumo - Veja um panorama geral das doações\n'\
            '/resumo_semanal - Um resumo das doações da última semana\n\n'\
            '/ultima_atualizacao - Verifique a última vez que a base de dados foi atualizada\n\n'\
            'Faça sua doação no site oficial: https://www.meepdonate.com/live/operacaofifa'
        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo":
        with db.engine.connect() as connection:
            result = connection.execute(
                'select sum(amount) amount, sum(quantity) quantity from donations')
            for row in result:
                amount = row[0]
                quantity = row[1]

        locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')
        amount_format = locale.currency(
            float(amount), grouping=True, symbol=None)

        message = f'💰 R$ {amount_format} foram doados até o momento.\n'\
            f'🦊 Ao todo foram {quantity} doações.\n\n'\
            'Faça sua doação no site oficial: https://www.meepdonate.com/live/operacaofifa'

        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/ultima_atualizacao":
        with db.engine.connect() as connection:
            result = connection.execute(
                "select date_last_request last_request from date_last_request")
            for row in result:
                last_update = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')

        time_delta = datetime.now()-last_update
        minutes_last_update = int(time_delta.total_seconds()/60)
        message = 'A nossa base de dados foi atulizada pela úlima vez há '\
            f'⏱ {minutes_last_update} minutos atrás.'

        bot.sendMessage(chat_id=chat_id, text=message,
                        reply_to_message_id=msg_id)

    elif text == "/resumo_semanal":
        with db.engine.connect() as connection:
            message = 'Este é um resumo das doações dos últimos sete dias:\n'\
                      'Data                    Valor\n'

            sum_amount = 0
            locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')
            result = connection.execute(
                """select substr(date,0,11)date, sum(amount) valor_doado from quantities
                   group by date
                   order by date DESC
                   limit 7""")
            for row in result:
                date_format = row[0][8:10]+'/'+row[0][5:7]+'/'+row[0][0:4]
                message += f'{date_format}         R$ {locale.currency(float(row[1]), grouping=True, symbol=None)}\n'
                sum_amount += float(row[1])
        message += '\nO total de doações dos últimos 7 dias foi de'\
            f'R$ {locale.currency(sum_amount, grouping=True, symbol=None)}'\
            '\n\nFaça sua doação no site oficial: https://www.meepdonate.com/live/operacaofifa'
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
    with db.engine.connect() as connection:
        result = connection.execute(
            'select sum(amount) amount, sum(quantity) quantity from donations')
        for row in result:
            amount = row[0]
            quantity = row[1]

    return jsonify({"amount": amount, "quantity": quantity})
