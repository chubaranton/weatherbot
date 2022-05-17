import src.city
import telebot
import time
from telebot import types
from telebot.types import Message, CallbackQuery
import src.magicconstants as mc

from os import environ


TOKEN = environ.get("API_KEY")
STICKER = mc.cherry

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    """Запускается при старте бота"""
    Greeting = mc.greeting
    if message.text == "/start":
        bot.send_sticker(message.chat.id, STICKER)
        bot.send_message(message.chat.id, Greeting, parse_mode='html')


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def reply_to_message(message: Message) -> None:
    """Выбор города"""
    weather = city.parse(message.text)
    if weather is None:
        send = mc.discourteous
        bot.send_message(message.chat.id, send)
    else:
        TEMPERATURE = weather[0]['temp']
        DESCRIPTION = weather[0]['description']
        FEELS_LIKE = weather[0]['feels like']
        PRESSURE = weather[0]['pressure']
        HUMIDITY = weather[0]['humidity']
        WIND = weather[0]['wind']
        send = f'<u>Температура:</u> {TEMPERATURE}\n{DESCRIPTION}'
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text=mc.details,
                                                     callback_data=f'{FEELS_LIKE},{WIND},{HUMIDITY},{PRESSURE}')
        keyboard.add(callback_button)
        bot.send_message(message.chat.id, send, parse_mode='html', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def detailed_weather(call: CallbackQuery) -> None:
    """Более подробные данные"""
    [FEELS_LIKE, WIND, HUMIDITY, PRESSURE] = (call.data).split(',')
    detailed_send = f'Чувствуется как: <b>{FEELS_LIKE}С</b>\n' \
                    f'Скорость ветра: <b>{WIND} м/c</b>\n' \
                    f'Влажность: <b>{HUMIDITY}%</b>\n' \
                    f'Давление: <b>{PRESSURE} мм</b>\n'
    bot.send_message(call.message.chat.id, detailed_send, parse_mode='html')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(e)
            time.sleep(15)
