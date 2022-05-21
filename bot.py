from TOKEN import token
import telebot
from telebot import types

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Tell me why......', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Tell me why......", reply_markup=markup)
#     bot.send_message(message.chat.id, f"Я пробил информацию:\n\n"
#                                       f" Id чата: {message.chat.id}\n"
#                                       f" Id пользователя: {message.from_user.id}\n"
#                                       f" Имя: {message.from_user.first_name}\n"
#                                       f" Фамилия: {message.from_user.last_name}\n"
#                                       f" Псевдоним: {message.from_user.username}\n\n"
#                                       f" Дата отправленного сообщения: {datetime.datetime.utcfromtimestamp(message.date)}\n\n"
#
#         startKBoard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
#         six_grade = types.KeyboardButton(text="6 класс")
#         seven_grade = types.KeyboardButton(text="7 класс")
#         eight_grade = types.KeyboardButton(text="8 класс")
#         nine_grade = types.KeyboardButton(text="9 класс")
#         startKBoard.add(six_grade, seven_grade, eight_grade, nine_grade)
#         bot.send_message(message.chat.id, "Выберите свой класс.", reply_markup=startKBoard)f"{message.text}")\

# @bot.message_handler(commands=['keyboard'])
# def keyboard_start(message):
#     startKBoard = types.ReplyKeyboardMarkup(row_width=1)
#     six_grade = types.KeyboardButton(text="6 класс")
#     seven_grade = types.KeyboardButton(text="7 класс")
#     startKBoard.add(six_grade, seven_grade)
#     bot.send_message(message.chat.id, "Выберите свой класс.", reply_markup=startKBoard)

# @bot.message_handler(func=lambda m: m.text == '1')
# def start(message):
#     bot.send_message(message.chat.id, '<b>Жирный</b>\n'
#                                       ' <i>Курсив</i>\n'
#                                       ' <u>Нижнее подчёркивание</u>\n'
#                                       ' <s>Зачёркнутый</s>\n'
#                                       ' <a href="https://stepik.org/course/107302/">Гиперссылка</a>\n'
#                                       '<tg-spoiler>Спойлер</tg-spoiler>', parse_mode='HTML')

# @bot.message_handler(commands=['add'])
# def add(message):
#     photo = open('л1.jpg','rb')
#     bot.send_photo(message.chat.id, photo)
# @bot.message_handler(func=lambda m: True, content_types=['text'])
# def text(message):
#     bot.send_message(message.chat.id, 'Это текст')
#
# @bot.message_handler(func=lambda m: True, content_types=['photo'])
# def photo(message):
#     bot.send_message(message.chat.id, 'Это фото')
#
# @bot.message_handler(func=lambda m: True, content_types=['video'])
# def video(message):
#     bot.send_message(message.chat.id, 'Это видео')
#
# @bot.message_handler(func=lambda m: True, content_types=['sticker'])
# def sticker(message):
#     bot.send_message(message.chat.id, 'Это стикер')
#
# @bot.message_handler(func=lambda m: True, content_types=['audio'])
# def audio(message):
#     bot.send_message(message.chat.id, 'Это аудио')

# @bot.message_handler(func=lambda m: True)
# def mad_bot(message):
#     bot.send_message(message.chat.id, message.text + ' - Чушь какая-то. Без негатива ' ' \U0001F921')

# @bot.message_handler(func=lambda m: True)
# def findThieves(message):
#     name = 'Edinaya Rossiya'
#     secret_symbol = ['$', '¥', '€']
#     message = message.text
#     n = 0
#     if name in message:
#         for symbol in secret_symbol:
#             if symbol in message:
#                 n += 1
#         if n != 0:
#             return True
#         else:
#             return False
#     else:
#         return False
#
# @bot.message_handler(func=lambda m: True)
# def findThieves(message):
#     name = ['Edinaya', 'Rossiya']
#     secret_symbol = ['$', '¥', '€']
#     message = message.text
#     lst = message.split(' ')
#     if name in lst:
#         for symbol in secret_symbol:
#             if symbol in lst:
#                 return True
#             else:
#                 return False

# @bot.message_handler(func=lambda m: m.text == 'Кот')
# def echo_all(message):
#     bot.reply_to(message, "Добро пожаловать в наше секретное кошачье общество, господин кот!")
#
# @bot.message_handler(func=lambda m: m.text == 'Мяу')
# def echo_all(message):
#     bot.reply_to(message, "Мяу, мяу!")

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, "Пароль?")

bot.polling()

