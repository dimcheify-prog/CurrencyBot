import requests
import json
from currency import currency

class APIExceptions(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote, base, amount):

        if quote == base:
            raise APIExceptions('Невозможно перевести одинаковые валюты')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIExceptions('Неправильно указана валюта')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIExceptions('Неправильно указана валюта')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExceptions('Неправильно указана сумма конвертации')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currency[base]]

        return total_base * amount