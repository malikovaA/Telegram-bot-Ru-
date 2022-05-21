from TOKEN import token
import telebot
from telebot import types
from telebot import util

bot = telebot.TeleBot(token)

# text = open('','r',encoding='utf8').read()
# for message1 in util.smart_split(text, 1000):   # метод util.smart_split позволяет присылать большие тексты
#     bot.send_message(message.chat.id, message1)


# @bot.message_handler()
# def name(message):
#     sent = bot.reply_to(message, '')
#     bot.register_next_step_handler(sent, rewiew)
# def review(message):
#     message_to_save = message.text

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в чат-бот по русскому языку для 6-9 классов!\n'
                                      'Данный бот поможет вам освежить свои знания в рамках школьной программы и проверить их с помощью тестов.\n'
                                      'Для продолжения работы <b> введите пароль </b>. \n'
                                      'Узнать его можно у своего преподавателя по русскому языку.', parse_mode='HTML')
    @bot.message_handler(func=lambda m: m.text == '01035')
    def start(message):
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        six_grade = types.InlineKeyboardButton(text='6 класс', callback_data='sig') #Выбор класса
        seven_grade = types.InlineKeyboardButton(text='7 класс', callback_data='seg')
        eight_grade = types.InlineKeyboardButton(text='8 класс', callback_data='eg')
        nine_grade = types.InlineKeyboardButton(text='9 класс', callback_data='ng')
        startKBoard.add(six_grade, seven_grade, eight_grade, nine_grade)
        bot.send_message(message.chat.id, 'Выберите свой класс.', reply_markup=startKBoard)

@bot.callback_query_handler(func=lambda callback: callback.data)
def subject(callback):
    if callback.data == 'sig':
        kb = types.InlineKeyboardMarkup(row_width=1)
        lexis = types.InlineKeyboardButton(text='ЛЕКСИКА', callback_data='lexis')
        word = types.InlineKeyboardButton(text='СЛОВООБРАЗОВАНИЕ', callback_data='word')
        orthography = types.InlineKeyboardButton(text='ОРФОГРАФИЯ', callback_data='orthography')
        parts_of_speech = types.InlineKeyboardButton(text='ЧАСТИ РЕЧИ', callback_data='parts_of_speech')
        kb.add(lexis, word, orthography, parts_of_speech)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите тему.',
                              reply_markup=kb)

def parts_of_speech(callback):
    if callback.data == 'parts_of_speech':
        prt = types.InlineKeyboardMarkup(row_width=1)
        theory = types.InlineKeyboardButton(text='ТЕОРИЯ', callback_data='theory')
        tests = types.InlineKeyboardButton(text='ТЕСТЫ', callback_data='tests')
        results = types.InlineKeyboardButton(text='РЕСУЛЬТАТЫ', callback_data='results')
        prt.add(theory, tests, results)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите раздел.',
                                  reply_markup=prt)
# @bot.callback_query_handler(func=lambda callback: callback.data)
# def parts_of_speech(callback):
#     if callback.data == 'parts_of_speech':
#         bot.send_message(message.chat.id, 'Добро пожаловать')
#         prt = types.InlineKeyboardMarkup(row_width=1)
#         theory = types.InlineKeyboardButton(text='ТЕОРИЯ', callback_data='theory')
#         tests = types.InlineKeyboardButton(text='ТЕСТЫ', callback_data='tests')
#         results = types.InlineKeyboardButton(text='РЕСУЛЬТАТЫ', callback_data='results')
#         prt.add(theory, tests, results)
#         bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите раздел.',
#                               reply_markup=prt)
bot.polling()