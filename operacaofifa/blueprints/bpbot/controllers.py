import pandas as pd
import requests
from operacaofifa.ext.database import db
from operacaofifa.ext.database_mongo import mongo
from datetime import datetime


def format_currency(valor):
    return "R$ " + (
        "{:,.2f}".format(valor).replace(",", " ").replace(".", ",").replace(" ", ".")
    )


def format_number(valor):
    return f"{valor:,}".replace(",", ".")


def update_data():
    req = requests.get(
        "https://meepserver.azurewebsites.net/api/Donate/Payments/F3289933-DB0A-45D7-A23A-E584191B2915"
    )
    data = req.json()

    data_req = {"date_last_request": [datetime.now()]}

    date_request = pd.DataFrame.from_dict(data_req)
    donations = pd.DataFrame(data["donations"])
    quantities = pd.DataFrame(data["quantities"])

    date_request.to_sql("date_last_request", con=db.engine, if_exists="replace")
    donations.to_sql("donations", con=db.engine, if_exists="replace")
    quantities.to_sql("quantities", con=db.engine, if_exists="replace")


def need_to_update():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(
                "select date_last_request from date_last_request"
            )
            for row in result:
                last_update = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")

                time_delta = datetime.now() - last_update
                minutes_last_update = int(time_delta.total_seconds() / 60)

        if minutes_last_update > 15:
            return True
        else:
            return False
    except:
        return True


def view_start():
    message = (
        "Olá seja bem vindo ao Bot da Operação FIFA\n\n"
        "Este bot é uma iniciativa de torcedores e não possui vínculo "
        "com a Meep e nem com o Cruzeiro.\n"
        "Uma solução de torcedores para torcedores em nome da transparência!\n\n"
        "🦊 NÓS SOMOS CRUZEIRO 🦊\n\n"
        "Você pode interagir com o bot com os seguintes comandos:\n"
        "/start - Iniciar o bot\n\n"
        "/resumo - Veja um panorama geral das doações\n"
        "/resumo_semanal - Um resumo das doações da última semana\n"
        "/resumo_mensal - Consolidado de doações por mês\n\n"
        "/ultima_atualizacao - Verifique a última vez que a base de dados foi atualizada\n\n"
        "Faça sua doação no site oficial: https://www.meepdonate.com/live/operacaofifa"
    )
    return message


def view_resume():
    with db.engine.connect() as connection:
        result = connection.execute(
            "select sum(amount) amount, sum(quantity) quantity from donations"
        )
        for row in result:
            amount = row[0]
            quantity = row[1]

    amount_format = format_currency(float(amount))
    quantity_format = format_number(quantity)

    message = (
        f"💰 {amount_format} foram doados até o momento.\n"
        f"🦊 Ao todo foram {quantity_format} doações.\n\n"
        "Faça sua doação no site oficial: https://www.meepdonate.com/live/operacaofifa"
    )
    return message


def view_week_summary():
    with db.engine.connect() as connection:
        message = (
            "Este é um resumo das doações dos últimos sete dias:\n"
            "Data                    Valor\n"
        )

        sum_amount = 0
        result = connection.execute(
            """select substr(date,0,11)date, sum(amount) valor_doado from quantities
                group by date
                order by date DESC
                limit 7"""
        )
        for row in result:
            date_format = row[0][8:10] + "/" + row[0][5:7] + "/" + row[0][0:4]
            message += f"{date_format}         {format_currency(float(row[1]))}\n"
            sum_amount += float(row[1])

    message += (
        "\nO total de doações dos últimos 7 dias foi de "
        f"{format_currency(sum_amount)}"
        "\n\nFaça sua doação no site oficial: https://www.meepdonate.com/live/operacaofifa"
    )

    return message


def view_month_summary():
    with db.engine.connect() as connection:
        message = (
            "Este é um resumo das doações por mês:\n" "Data                   Valor\n"
        )

        sum_amount = 0
        result = connection.execute(
            """select substr(date,0,8) date, sum(amount) valor_doado from quantities
               group by substr(date,0,8)
            """
        )
        for row in result:
            date_format = row[0][5:7] + "/" + row[0][0:4]
            message += f"{date_format}            {format_currency(float(row[1]))}\n"
            sum_amount += float(row[1])

    message += (
        "\nO total de doações foi de "
        f"{format_currency(sum_amount)}"
        "\n\nFaça sua doação no site oficial: https://www.meepdonate.com/live/operacaofifa"
    )

    return message


def view_last_update():
    with db.engine.connect() as connection:
        result = connection.execute(
            "select date_last_request last_request from date_last_request"
        )
        for row in result:
            last_update = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")

    time_delta = datetime.now() - last_update
    minutes_last_update = int(time_delta.total_seconds() / 60)
    message = (
        "A nossa base de dados foi atulizada pela última vez há "
        f"⏱ {minutes_last_update} minutos atrás."
    )
    return message


def register_log(username, first_name, text, is_bot):
    mongo.db.logs.insert_one(
        {
            "username": username,
            "first_name": first_name,
            "text": text,
            "is_bot": is_bot,
            "datetime": requests.get(
                "http://worldtimeapi.org/api/timezone/America/Sao_Paulo"
            ).json()["datetime"],
        }
    )
