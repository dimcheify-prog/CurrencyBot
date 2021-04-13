import telebot
from auth import TOKEN #create the 'auth' file and import your own telegram token
from currency import currency
from extencions import CryptoConverter, APIExceptions


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def info(message):
    text = '<имя валюты, цену которой он хочет узнать> ' \
           '<имя валюты, в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты> /value чтобы узнать список доступных валют'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['value'])
def value(message):
    text = 'Доступные валюты: '
    for i in currency.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message):

    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise APIExceptions('Должно быть 3 параметра')

        quote, base, amount = value

        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIExceptions as e:
        bot.reply_to(message, f'Ошибка пользователя {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду {e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} - {total_base}.'
        bot.send_message(message.chat.id, text)


bot.polling()
