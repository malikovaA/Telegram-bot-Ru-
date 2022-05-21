from TOKEN import token
import telebot
from telebot import types
from random import randint

bot = telebot.TeleBot(token)

# text = open('','r',encoding='utf8').read()
# for message1 in util.smart_split(text, 1000):   # метод util.smart_split позволяет присылать большие тексты
#     bot.send_message(message.chat.id, message1)

# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_poll(message.chat.id, question='Как дела?', options=['Хорошо', 'Нормально', 'Плохо'],
#                   allows_multiple_answers=False, is_anonymous=True)

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
    count = 0
    if callback.data in ['sig', 'seg', 'eg', 'ng', 'back']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        lexis = types.InlineKeyboardButton(text='ЛЕКСИКА', callback_data='lexis')
        word = types.InlineKeyboardButton(text='СЛОВООБРАЗОВАНИЕ', callback_data='word')
        orthography = types.InlineKeyboardButton(text='ОРФОГРАФИЯ', callback_data='orthography')
        parts_of_speech = types.InlineKeyboardButton(text='ЧАСТИ РЕЧИ', callback_data='parts_of_speech')
        kb.add(lexis, word, orthography, parts_of_speech)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите тему.',
                              reply_markup=kb)
        count = 0
    if callback.data in ['parts_of_speech', 'lexis', 'word', 'orthography']:
        prt = types.InlineKeyboardMarkup(row_width=1)
        theory = types.InlineKeyboardButton(text='ТЕОРИЯ', callback_data='theory')
        tests = types.InlineKeyboardButton(text='ТЕСТЫ', callback_data='tests')
        results = types.InlineKeyboardButton(text='РЕЗУЛЬТАТЫ', callback_data='results')
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        prt.add(theory, tests, results, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите раздел.',
                                  reply_markup=prt)
    if callback.data == 'theory':
        sources = types.InlineKeyboardMarkup(row_width=1)
        theory = types.InlineKeyboardButton(text='Тема 1', url='https://yandex.ru/')
        tests = types.InlineKeyboardButton(text='Тема 2', url='https://www.google.com/')
        results = types.InlineKeyboardButton(text='Тема 3', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        sources.add(theory, tests, results, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Ознакомтесь с источниками.',
                                  reply_markup=sources)
    if callback.data == 'results':
        text = f'Результат последнего теста {randint(0,10)} баллов'
        sources = types.InlineKeyboardMarkup(row_width=1)
        theory = types.InlineKeyboardButton(text='Общий результат 9/10, так держать!', url='https://www.youtube.com/watch?v=RcOcjF-iT6w')
        test_last = types.InlineKeyboardButton(text=text, callback_data='nice')
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        sources.add(theory, test_last, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Вы - капитальный красавчик.',
                                  reply_markup=sources)
    if callback.data == 'tests':
        sources = types.InlineKeyboardMarkup(row_width=1)
        test1 = types.InlineKeyboardButton(text='Блок тестов', url='https://yandex.ru/tutor/subject/?subject_id=3')
        test2 = types.InlineKeyboardButton(text='Контрольный тест', callback_data='finish_test')
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        sources.add(test1, test2, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберете тест для прохождения.',
                                  reply_markup=sources)
    if callback.data == 'finish_test':
        sources = types.InlineKeyboardMarkup(row_width=1)
        test1 = types.InlineKeyboardButton(text='Большая загадка', callback_data='finish_test_1')
        test2 = types.InlineKeyboardButton(text='Катастрофа для всех', callback_data='finish_test_1')
        test3 = types.InlineKeyboardButton(text='Ответственный зверь', callback_data='finish_test_1')
        back = types.InlineKeyboardButton(text='Вернуться в меню', callback_data='back')
        sources.add(test1, test2, test3, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Рыба - это...',
                                  reply_markup=sources)
        count += 1
    if callback.data == 'finish_test_1':
        sources = types.InlineKeyboardMarkup(row_width=1)
        test1 = types.InlineKeyboardButton(text='Андатра', callback_data='finish_test_2')
        test2 = types.InlineKeyboardButton(text='Ондатра', callback_data='finish_test_2')
        back = types.InlineKeyboardButton(text='Вернуться в меню', callback_data='back')
        sources.add(test1, test2, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выбери правильный вариант:',
                                  reply_markup=sources)
        count += 1
    if callback.data == 'finish_test_2':
        sources = types.InlineKeyboardMarkup(row_width=1)
        test1 = types.InlineKeyboardButton(text='Это полуводный грызун родом из Северной Америки', callback_data='results')
        test2 = types.InlineKeyboardButton(text='Вид млекопитающих из подсемейства полёвок семейства хомяковых', callback_data='results')
        test3 = types.InlineKeyboardButton(text='Ответственный зверь из семейства хомяковых', callback_data='results')
        back = types.InlineKeyboardButton(text='Вернуться в меню', callback_data='back')
        sources.add(test1, test2, test3, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Что означает слово "Андатра?',
                                  reply_markup=sources)
        count += 1

bot.polling()