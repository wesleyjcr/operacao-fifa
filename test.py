text = '/feedback gostei do aplicativo'


def validar(text):
    if '/feedback' in text:
        print('Sim')
    return text


print(validar(text))
