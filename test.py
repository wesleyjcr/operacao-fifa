valor = 652438


def format_currency(valor):
    valor = 'R$ ' + ('{:,.2f}'.format(valor)
                     .replace(',', ' ')
                     .replace('.', ',')
                     .replace(' ', '.'))

    return valor


def format_number(valor):
    return f'{valor:,}'.replace(',', '.')


print(format_number(valor))
