# конвертирует в бел рубли

import json
import telebot
import requests

token = '5964559637:AAFzIyiMImcue0INMap0PbpmG9X1mrqxXm0'
bot = telebot.TeleBot(token)


def get_course(currency):
    response = requests.get(f'https://www.nbrb.by/api/exrates/rates/{currency}?parammode=2')
    data = json.loads(response.text)
    if data['Cur_Scale'] == 100:
        rez = (data['Cur_OfficialRate']) / 100
    else:
        rez = data['Cur_OfficialRate']
    return rez


def count_course(course, amount):
    try:
        c = float(course)
        n = float(amount)
        return round(c * n, 3)
    except ValueError:
        return 'Неверный ввод, попробуйте еще раз.'


@bot.message_handler(commands=['start'])
def hello_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = ['USD', 'EUR', 'RUB']
    for i in buttons:
        markup.add(telebot.types.KeyboardButton(i))

    bot.send_message(message.chat.id, 'Привет! Выбери валюту для конверсии.', reply_markup=markup)


@bot.message_handler(content_types='text')
def receive_message(message):
    curr = ['USD', 'EUR', 'RUB']
    try:
        if message.text == 'USD':
            course = get_course('USD')
            amount = 'Введите сумму в USD:'
        elif message.text == 'EUR':
            course = get_course('EUR')
            amount = 'Введите сумму в EUR:'
        elif message.text == 'RUB':
            course = get_course('RUB')
            amount = 'Введите сумму в RUB:'
        elif message.text not in curr:

            bot.send_message(message.chat.id, 'Неверный ввод, попробуйте еще раз.')
        else:
            return

        msg = bot.send_message(message.chat.id, amount)
        bot.register_next_step_handler(msg, lambda message: send_amount(message, course))

    except Exception as e:
        bot.reply_to(message, 'При выборе валюты воспользуйтесь кнопками.')


def send_amount(message, course):
    try:
        result = count_course(course, message.text)
        bot.reply_to(message, f'Результат конверсии: {result} BYN')
    except ValueError:
        bot.send_message(message, 'Неверный ввод, попробуйте еще раз.')


bot.polling()
