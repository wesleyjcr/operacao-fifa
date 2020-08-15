import requests

data = requests.get(
    'http://worldtimeapi.org/api/timezone/America/Sao_Paulo').json()['datetime']
print(data)
