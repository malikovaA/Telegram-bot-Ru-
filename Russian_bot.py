from TOKEN import token
import telebot
from telebot import types
from random import randint
from db import db_worker, sqlalch

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в чат-бот по русскому языку для 6-9 классов!\n'
                                      'Данный бот поможет вам освежить свои знания в рамках школьной программы и проверить их с помощью тестов.\n'
                                      'Для продолжения работы <b> введите пароль </b>. \n'
                                      'Узнать его можно у своего преподавателя по русскому языку.\n'
                                      'Для ученика пароль 1111, для учителя 0000.', parse_mode='HTML')
    @bot.message_handler(func=lambda m: m.text == '1111')
    def start(message):
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        startKBoard.add(*[types.InlineKeyboardButton(text=name, callback_data='back') for name in db_worker.grades])
        bot.send_message(message.chat.id, 'Выберите свой класс.', reply_markup=startKBoard)

    @bot.message_handler(func=lambda m: m.text == '0000')
    def start(message):
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        startKBoard.add(*[types.InlineKeyboardButton(text=name, callback_data='teacher') for name in db_worker.grades])
        bot.send_message(message.chat.id, 'Здравствуйте, учитель, выберите класс.', reply_markup=startKBoard)

@bot.callback_query_handler(func=lambda callback: callback.data)
def subject(callback):
    count = 0

    """ Главное меню для учителя """
    if callback.data in ['teacher', 'back_t']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        stat = types.InlineKeyboardButton(text='Статистика', callback_data='stat_t')
        theme = types.InlineKeyboardButton(text='Выберите тему', callback_data='theme_choose_t')
        add_theme = types.InlineKeyboardButton(text='Добавить тему', callback_data='add_theme')
        kb.add(stat, theme, add_theme)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите опцию.',
                              reply_markup=kb)
        """ Статистика по классу """
    if callback.data in ['stat_t']:
        text = f'Тестовый текст с результатами класса.\nУ вас всё в шоколаде {10}/{10}'
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='Назад', callback_data='back_t')
        kb.add(back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                              reply_markup=kb)

        """ Добавление темы """
    if callback.data in ['add_theme']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='Назад', callback_data='back_t')
        kb.add(back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Введите название темы',
                              reply_markup=kb)

        """ Меню с выбором тем для взаимодействия"""
    if callback.data in ['theme_choose_t']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='Назад', callback_data='back_t')
        kb.add(*[types.InlineKeyboardButton(text=name, callback_data='theme_t') for name in db_worker.themes])
        kb.add(back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите тему.',
                              reply_markup=kb)

        """ Меню с выбором опций по взаимодействию с выбранной темой """
    if callback.data in ['theme_t']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        delete = types.InlineKeyboardButton(text='Удалить тему', callback_data='delete_t')
        import_t = types.InlineKeyboardButton(text='Добавить тест', callback_data='import_t')
        stat = types.InlineKeyboardButton(text='Статистика по теме', callback_data='stat_t_theme')
        test_t = types.InlineKeyboardButton(text='Выбор теста', callback_data='test_t')
        back_t = types.InlineKeyboardButton(text='Назад', callback_data='back_t')
        kb.add(import_t, stat, delete, test_t,back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Выберите, что нужно сделать для этой темы. ',
                              reply_markup=kb)

        """ Раздел для импорта теста """
    if callback.data in ['import_t']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='Назад', callback_data='back_t')
        kb.add(back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Добавьте файл установленного формата с тестом',
                              reply_markup=kb)
        """
        Тут будет функция для импорта теста из sql_methods.py
        
        @bot.message_handler(content_types=['document'])
        def handle_docs_photo(message):
            try:
                chat_id = message.chat.id

                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = 'files/' + message.document.file_name
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)


                bot.reply_to(message, "Пожалуй, я сохраню это")
            except Exception as e:
                bot.reply_to(message, e)
        """


        """ Раздел со статистикой по теме """
    if callback.data in ['stat_t_theme']:
        text = f'Тестовый текст с результатами по теме.\nУ вас всё в шоколаде {10}/{10}'
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='Назад', callback_data='back_t')
        kb.add(back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                              reply_markup=kb)

        """ Меню для просмотра / удаления теста """
    if callback.data in ['test_t']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        text = f'Тестовый текст с потенциальным названием теста'
        delete = types.InlineKeyboardButton(text='Удалить тест', callback_data='delete_t')
        back_t = types.InlineKeyboardButton(text='Назад', callback_data='back_t')
        kb.add(delete, back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text=text,
                              reply_markup=kb)

        """ Главное меню для ученика """
    if callback.data in ['back']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(*[types.InlineKeyboardButton(text=name, callback_data='theme_s') for name in db_worker.themes])
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите тему.',
                              reply_markup=kb)
        count = 0
        """ Меню с выбором раздела по теме """
    if callback.data in ['theme_s']:
        prt = types.InlineKeyboardMarkup(row_width=1)
        theory = types.InlineKeyboardButton(text='ТЕОРИЯ', callback_data='theory')
        tests = types.InlineKeyboardButton(text='ТЕСТЫ', callback_data='tests')
        results = types.InlineKeyboardButton(text='РЕЗУЛЬТАТЫ', callback_data='results')
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        prt.add(theory, tests, results, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите раздел.',
                                  reply_markup=prt)

        """ Вкладка с теорией """
    if callback.data == 'theory':
        sources = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        sources.add(*[types.InlineKeyboardButton(text=k, url=v) for k,v in zip(db_worker.theory_titles, db_worker.theory_content)])
        sources.add(back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Ознакомтесь с источниками.',
                                  reply_markup=sources)

        """ Раздел для просмотра результатов """
    if callback.data == 'results':
        text = f'Результат последнего теста {randint(0,10)} баллов'
        sources = types.InlineKeyboardMarkup(row_width=1)
        theory = types.InlineKeyboardButton(text='Общий результат 9/10, так держать!', url='https://www.youtube.com/watch?v=RcOcjF-iT6w')
        test_last = types.InlineKeyboardButton(text=text, callback_data='nice')
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        sources.add(theory, test_last, back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Вы - капитальный красавчик.',
                                  reply_markup=sources)

        """ Вкладка для выбора теста 
        Но тут еще надо будет внести правки 
        по принципу работы тестов        
        """
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