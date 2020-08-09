'''
Capturar dados do site
Inserir em um banco de dados 
    Tabelas
        Ultima atualização
        Donations
        Quantidades

    Total doado por dia
    Total doado por mês
    Gráfico com valores
'''

from datetime import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


engine = create_engine('sqlite:///storage.db', echo=False)


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


with engine.connect() as connection:
    result = connection.execute(
        'select date_last_request from date_last_request')
    for row in result:
        last_update = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')

        time_delta = datetime.now()-last_update
        minutes_last_update = int(time_delta.total_seconds()/60)

if minutes_last_update > 60:
    update_data()


# x = df1['date']
# y = df1['amount']
# plt.plot(x, y)
# plt.savefig('teste.png')
