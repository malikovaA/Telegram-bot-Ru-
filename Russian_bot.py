from TOKEN import token
import telebot
from telebot import types
# from db import db_worker # тут был вариант с реализацией через rawSQL (сырой SQL код)
from db_pack import sqlalch as sql
from db_pack.sql_methods import get_or_create, export_test_theme, export_test_class
from datetime import datetime
import os
from random import randint

bot = telebot.TeleBot(token)
student_name = ''
answer_counter = 0
student_result = 0
test_id_special = 0
theme_titles = [i[0] for i in sql.session.query(sql.Theme.title).all()]


@bot.message_handler(commands=['start'])
def start(message):
    global student_name, theme_titles

    bot.send_message(message.chat.id, 'Добро пожаловать в чат-бот по русскому языку для 6-9 классов!\n'
                                      'Данный бот поможет вам освежить свои знания в рамках школьной программы и проверить их с помощью тестов.\n\n'
                                      'Для доступа к тренажеру (тесты по различным темам) отправьте в чат <b>"тренажер"</b>.\n\n'
                                      'Для продолжения работы в роли родителя, ученика иди учителя<b> введите соответствующий пароль </b>. \n'
                                      'Узнать его можно у своего преподавателя по русскому языку.\n\n'
                                      'Для ученика пароль 1111, для учителя 0000, для родителя 2222.', parse_mode='HTML')

    ls = [i[0] for i in sql.session.query(sql.Class.title).all()]
    student_name = f'{message.from_user.first_name} {message.from_user.last_name}'

    @bot.message_handler(func=lambda m: m.text in ['тренажер','тренажёр','Тренажер','Тренажёр'])
    def start(message):
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        startKBoard.add(
            *[types.InlineKeyboardButton(text=title, callback_data=f'training{id+1}') for id, title in enumerate(theme_titles)])
        bot.send_message(message.chat.id, 'Выберите тему.', reply_markup=startKBoard)

    @bot.message_handler(func=lambda m: m.text == '1111')
    def start(message):
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        startKBoard.add(
            *[types.InlineKeyboardButton(text=title, callback_data=str(ls.index(title) + 1)) for title in ls])
        bot.send_message(message.chat.id, 'Выберите свой класс.', reply_markup=startKBoard)

    @bot.message_handler(func=lambda m: m.text == '0000')
    def start(message):
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        startKBoard.add(
            *[types.InlineKeyboardButton(text=title, callback_data='class' + str(ls.index(title) + 1)) for title in ls])
        bot.send_message(message.chat.id, 'Здравствуйте, учитель, выберите класс.', reply_markup=startKBoard)

    @bot.message_handler(func=lambda m: m.text == '2222')
    def start(message):
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        add_parent = types.InlineKeyboardButton(text='Подтвердить роль родителя', callback_data='add_parent')
        startKBoard.add(add_parent)
        bot.send_message(message.chat.id, 'Здравствуйте, родитель, подтвердите выбор роли.\n',
                         reply_markup=startKBoard)


@bot.callback_query_handler(func=lambda callback: callback.data)
def subject(callback):
    global student_name, answer_counter, student_result, test_id_special, theme_titles
    count = 0
    back__ = 0
    count_t = 0
    back_track = 0
    back_back_ = 0
    theory_titles = [i[0] for i in sql.session.query(sql.Theory.title).all()]
    theory_content = [i[0] for i in sql.session.query(sql.Theory.content).all()]
    results_ = [i[0] for i in sql.session.query(sql.Result.id).all()]
    tests_ = [i[0] for i in sql.session.query(sql.Test_name.title).all()]
    questions = [i[0] for i in sql.session.query(sql.Test_question.id).all()]
    ls = [i[0] for i in sql.session.query(sql.Class.title).all()]

    """ Родитель. """
    if callback.data == 'add_parent':
        try:
            parent_id = callback.message.chat.id
            parent = sql.Parent(id=parent_id)
            already_exist = sql.session.query(sql.Parent).get(parent.id)
            if already_exist:
                pass
            else:
                sql.session.add(parent)
            sql.session.commit()
            # get_or_create(sql.session, sql.Student, id=callback.message.chat.id, name=student_name, class_id=student_class)
        finally:
            startKBoard = types.InlineKeyboardMarkup(row_width=1)
            show_results = types.InlineKeyboardButton(text='Посмотреть результаты', callback_data='show_results')
            print_child_id = types.InlineKeyboardButton(text='Ввести id ребёнка', callback_data='print_child_id')
            startKBoard.add(show_results, print_child_id)
            text = 'Здравствуйте, родитель, выберите опцию.\n' \
                   'Сначала необходимо ввести id ребёнка, если вы ранее этого не сделали.\n' \
                   'Иначе опция просмотра результатов будет недоступна.'
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text=text,
                                  reply_markup=startKBoard)

    """ Родитель. Ввод id ребёнка. """
    if callback.data == 'print_child_id':
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_p = types.InlineKeyboardButton(text='Назад', callback_data='add_parent')
        kb.add(back_p)

        @bot.message_handler(content_types=["text"])
        def create_theme(message):
            parent = sql.session.query(sql.Parent).get(message.chat.id)
            parent.student_id = int(message.text)
            sql.session.commit()
            bot.send_message(message.chat.id, f'ID ребёнка - {message.text} добавлено,'
                                              f' вы можете посмотреть его результаты!',reply_markup=kb)

        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Отправьте в чат id своего ребёнка для установления связи между вашими профилями.',
                              reply_markup=kb)


    """ Родитель. Просмотр результатов. """
    if callback.data == 'show_results':
        parent = sql.session.query(sql.Parent).get(callback.message.chat.id)
        result = sql.session.query(sql.Result.result, sql.Test_name.title).join(sql.Test_name) \
            .join(sql.Theme).filter(sql.Result.student_id == parent.student_id)
        result_value = [i[0] for i in result]
        result_name = [i[1] for i in result]
        sources = types.InlineKeyboardMarkup(row_width=1)
        text = 'Ознакомтесь с результатами:\n'
        for v, n in zip(result_value, result_name):
            text += f'За тест {n} набранно {v} баллов.\n'
            # sources.add(types.InlineKeyboardButton(text=text))
        back_p = types.InlineKeyboardButton(text='Назад', callback_data='add_parent')
        sources.add(back_p)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                              reply_markup=sources)


    """ Тренажер. Вкладка для выбора темы """
    if callback.data == 'training_back':
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        startKBoard.add(
            *[types.InlineKeyboardButton(text=title, callback_data=f'training{id}') for id, title in
              enumerate(theme_titles)])
        bot.send_message(callback.message.chat.id, 'Выберите тему.', reply_markup=startKBoard)

    """ Тренажер. Вкладка для выбора теста """
    for i in range(1, len(theme_titles) + 1):
        if callback.data == f'training{i}':
            test_by_theme = sql.session.query(sql.Test_name.title, sql.Test_name.id) \
                .join(sql.Theme).filter(sql.Theme.id == i)
            tests_titles = [i[0] for i in test_by_theme]
            tests_id = [i[1] for i in test_by_theme]
            sources = types.InlineKeyboardMarkup(row_width=1)
            sources.add(
                *[types.InlineKeyboardButton(text=title, callback_data=f'training_question{id}')
                  for title, id in zip(tests_titles, tests_id)])
            interest = types.InlineKeyboardButton(text='Интересные факты', callback_data=f'interest')
            back = types.InlineKeyboardButton(text='Назад к выбору темы', callback_data='training_back')
            sources.add(interest, back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Выберете тест для прохождения.',
                                  reply_markup=sources)

    """Тренажёр. Вкладка с интересными фактами """
    if callback.data == f'interest':
            interest_content_ = [i[0] for i in sql.session.query(sql.Interesting.content)]
            sources = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(text='Назад', callback_data='training_back')
            sources.add(back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Интересные факты.')
            text = interest_content_[randint(0, len(interest_content_) - 1)]
            bot.send_message(chat_id=callback.message.chat.id, text=text,
                                  reply_markup=sources)

    """Тренажер. Вкладка для вопросов и ответов """
    for i in range(1, len(tests_) + 1):
        if callback.data == f'training_question{i}':
            test_id_special = i
            questions_by_test = sql.session.query(sql.Test_question.content, sql.Test_question.id) \
                .join(sql.Test_name).filter(sql.Test_name.id == i)
            questions_by_test_ = [i[0] for i in questions_by_test]
            questions_by_test_id = [i[1] for i in questions_by_test]
            text = f'Можете попрактиковаться:\n'

            for question, id in zip(questions_by_test_, questions_by_test_id):
                answers_by_test = sql.session.query(sql.Test_answer.content, sql.Test_answer.right) \
                    .join(sql.Test_question, sql.Test_question.id == sql.Test_answer.test_q_id) \
                    .filter(sql.Test_answer.test_q_id == id)
                answers_by_test_ = [j[0] for j in answers_by_test]
                answers_by_test_isright = [j[1] for j in answers_by_test]
                right_answer_id = answers_by_test_isright.index(1)
                bot.send_poll(callback.message.chat.id, question, answers_by_test_,
                              type='quiz', correct_option_id=right_answer_id)

            sources = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(text='Назад к выбору темы', callback_data='training_back')
            sources.add(back)
            bot.send_message(callback.message.chat.id, text, reply_markup=sources)


    """ Повторный выбор класса для учителя """
    if callback.data == 'choose_class':
        startKBoard = types.InlineKeyboardMarkup(row_width=1)
        startKBoard.add(
            *[types.InlineKeyboardButton(text=title, callback_data='class' + str(ls.index(title) + 1)) for title in ls])
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Выберите класс.',
                              reply_markup=startKBoard)

    """ Главное меню для учителя """
    for i in range(1,5):
        if callback.data in [f'class{i}', f'back_t{i}']:
            if count_t == 0:
                count_t = i
            kb = types.InlineKeyboardMarkup(row_width=1)
            stat = types.InlineKeyboardButton(text='Статистика', callback_data=f'stat_t{i}')
            theme = types.InlineKeyboardButton(text='Выберите тему', callback_data='theme_choose_t')
            add_theme = types.InlineKeyboardButton(text='Добавить тему', callback_data='add_theme')
            choose_class = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
            send_something = types.InlineKeyboardButton(text=f'Сделать рассылку для {i+5} класса', callback_data=f'send_something{i}')
            kb.add(stat, theme, add_theme, send_something, choose_class)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Выберите опцию.',
                                  reply_markup=kb)

    """ Создание рассылки """
    for i in range(1,5):
        if callback.data in [f'send_something{i}']:
            text = f'Напишите в чат сообщение, которые нужно отправить в рассылку {i+5} классу.'
            choose_class = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
            kb = types.InlineKeyboardMarkup(row_width=1)
            kb.add(choose_class)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text=text,
                                  reply_markup=kb)

            @bot.message_handler(content_types=["text"])
            def send_message_to_class(message):
                # students_id_from_class = sql.session.query(sql.Student.id).filter(sql.Student.class_id==i)
                # students_id_from_class = [j[0] for j in students_id_from_class]
                # for id in students_id_from_class:
                #     bot.send_message(id, f'{message.text}')
                text_message = f'Рассылка вида:\n{message.text}\nУспешно отправлена!'
                bot.send_message(callback.message.chat.id, text=text_message,
                                 reply_markup=kb)

        """ Статистика по классу """
    for i in range(1,5):
        if callback.data in [f'stat_t{i}']:
            result = sql.session.query(sql.Result.result, sql.Test_name.title, sql.Student.name, sql.Theme.title) \
                .select_from(sql.Result).join(sql.Test_name).join(
                sql.Theme).join(sql.Student).filter(sql.Student.class_id == i)
            result_v = [i[0] for i in result]
            result_theme = [i[3] for i in result]
            result_test = [i[1] for i in result]
            result_student = [i[2] for i in result]
            text = f'Результаты по {i + 6} классу следущие:\n'
            for v, theme, test, student in zip(result_v, result_theme, result_test, result_student):
                text += f'Ученик - {student}, Тема - {theme}, Тест - {test}, Результат - {v};\n\n'
            kb = types.InlineKeyboardMarkup(row_width=1)
            back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
            kb.add(back_t)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                  reply_markup=kb)
            file = export_test_class(result)
            with open(file, "rb") as f:
                f = f.read()
                bot.send_document(callback.message.chat.id, document=f,
                                  visible_file_name=f'Статистика_по_классу_{datetime.today()}.xlsx')
            os.remove(file)

        """ Добавление темы """
    if callback.data in ['add_theme']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
        kb.add(back_t)

        @bot.message_handler(content_types=["text"])
        def create_theme(message):
            new_theme = sql.Theme(title=message.text)
            sql.session.add(new_theme)
            sql.session.commit()
            bot.send_message(message.chat.id, f'Тема {message.text} создана!')

        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Отправьте в чат название новой темы, она будет создана автоматически.',
                              reply_markup=kb)

        """ Меню с выбором тем для взаимодействия"""
    if callback.data in ['theme_choose_t']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
        kb.add(*[types.InlineKeyboardButton(text=title, callback_data='theme_t' + str(theme_titles.index(title) + 1))
                 for title in theme_titles])
        kb.add(back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберите тему.',
                              reply_markup=kb)

        """ Меню с выбором опций по взаимодействию с выбранной темой """
    for i in range(len(theme_titles) + 1):
        if callback.data in [f'theme_t{i}']:
            kb = types.InlineKeyboardMarkup(row_width=1)
            delete = types.InlineKeyboardButton(text='Удалить тему', callback_data=f'delete_t{i}')
            import_t = types.InlineKeyboardButton(text='Добавить тест', callback_data=f'import_t{i}')
            stat = types.InlineKeyboardButton(text='Статистика по теме', callback_data=f'stat_t_theme{i}')
            test_t = types.InlineKeyboardButton(text='Выбор теста', callback_data=f'test_t{i}')
            back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
            back_back = types.InlineKeyboardButton(text='Назад', callback_data='theme_choose_t')
            kb.add(import_t, stat, delete, test_t, back_t, back_back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Выберите, что нужно сделать для этой темы. ',
                                  reply_markup=kb)

        """ Раздел для импорта теста """
    if callback.data in ['import_t']:
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
        kb.add(back_t)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Добавьте файл установленного формата с тестом',
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
    for i in range(len(theme_titles) + 1):
        if callback.data in [f'stat_t_theme{i}']:
            result = sql.session.query(sql.Result.result, sql.Student.name, sql.Student.class_id, sql.Theme.title,
                                       sql.Test_name.title).select_from(sql.Result).join(sql.Student,
                                                                                         sql.Student.id == sql.Result.student_id).join(
                sql.Test_name, sql.Test_name.id == sql.Result.test_id).join(sql.Theme,
                                                                            sql.Theme.id == sql.Test_name.theme_id).filter(
                sql.Theme.id == i)
            result_v = [i[0] for i in result]
            result_class = [i[2] for i in result]
            result_test = [i[4] for i in result]
            result_student = [i[1] for i in result]
            text = f'Результаты по теме {result[0][4]} среди всех классов следующие:\n'
            for v, c, test, student in zip(result_v, result_class, result_test, result_student):
                text += f'Ученик - {student}, класс - {c + 5}, Тест - {test}, Результат - {v};\n'
            kb = types.InlineKeyboardMarkup(row_width=1)
            back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
            back_back = types.InlineKeyboardButton(text='Назад', callback_data=f'theme_t{i}')
            kb.add(back_t, back_back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                  reply_markup=kb)
            file = export_test_theme(result)
            with open(file, "rb") as f:
                f = f.read()
                bot.send_document(callback.message.chat.id, document=f, visible_file_name=f'Результаты_по_теме_{datetime.today()}.xlsx')
            os.remove(file)


        """ Меню для просмотра списка тестов """
    for i in range(len(theme_titles) + 1):
        if callback.data in [f'test_t{i}']:
            if back__ == 0:
                back__ = i
            kb = types.InlineKeyboardMarkup(row_width=1)
            tests_for_theme = sql.session.query(sql.Test_name.title, sql.Theme.title).join(sql.Theme).filter(
                sql.Theme.id == i)
            tests_for_theme_ = [i[0] for i in tests_for_theme]
            text = f'Список тестов по теме {tests_for_theme[0][1]}:\n'
            back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
            back_back = types.InlineKeyboardButton(text='Назад', callback_data=f'theme_t{i}')
            kb.add(back_t, back_back)
            kb.add(*[
                types.InlineKeyboardButton(text=title, callback_data='test_q' + str(tests_for_theme_.index(title) + 1))
                for title in tests_for_theme_])
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text=text,
                                  reply_markup=kb)

    """ Меню для просмотра списка вопросов теста + удаление теста """
    for i in range(len(tests_) + 1):
        if callback.data in [f'test_q{i}']:
            if back_back_ == 0:
                back_back_ = i
            kb = types.InlineKeyboardMarkup(row_width=1)
            q_for_test = sql.session.query(sql.Test_question.content).filter(
                sql.Test_question.id == i)
            q_for_test = [i[0] for i in q_for_test]
            text = f'Список вопросов по тесту :\n'
            for i in q_for_test:
                text += f'{i}\n'
            back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
            back_back = types.InlineKeyboardButton(text='Назад', callback_data=f'test_t{back__}')
            delete = types.InlineKeyboardButton(text='Удалить этот тест', callback_data='delete_test')
            kb.add(back_t, back_back, delete)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text=text,
                                  reply_markup=kb)

    """ Меню для удаления теста """
    if callback.data == 'delete_test':
        kb = types.InlineKeyboardMarkup(row_width=1)
        back_t = types.InlineKeyboardButton(text='К выбору класса', callback_data='choose_class')
        back_back = types.InlineKeyboardButton(text='Назад', callback_data=f'test_q{back_back_}')
        kb.add(back_t, back_back)

        @bot.message_handler(content_types=["text"])
        def delete_test(message):
            test_for_delete = get_or_create(sql.session, sql.Test_name, title=message.text)
            # sql.session.query(sql.Test_name).filter(sql.Test_name.title==message.text).one()
            ''' тут *** вывод сообщения при неправильном вводе названия'''
            if test_for_delete:
                sql.session.delete(test_for_delete)
                sql.session.commit()
                bot.send_message(message.chat.id, f'Тест {message.text} удалён!')
            else:
                bot.send_message(message.chat.id, f'Тест {message.text} не найден.')

        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Отправьте в чат точное название теста, чтобы подтвердить удаление.',
                              reply_markup=kb)

        """ Главное меню для ученика """
    if callback.data in ['back', '1', '2', '3', '4']:
        back_track = 0
        try:
            if callback.data in ['1', '2', '3', '4']:
                student_class = int(callback.data)
                student = sql.Student(id=callback.message.chat.id, name=student_name, class_id=student_class)
                already_exist = sql.session.query(sql.Student).get(student.id)
                if already_exist:
                    already_exist.class_id = student_class
                else:
                    sql.session.add(student)
                sql.session.commit()
                # get_or_create(sql.session, sql.Student, id=callback.message.chat.id, name=student_name, class_id=student_class)
        finally:
            kb = types.InlineKeyboardMarkup(row_width=1)
            kb.add(
                *[types.InlineKeyboardButton(text=title, callback_data=f'theme_s{str(theme_titles.index(title) + 1)}')
                  for title in theme_titles])
            my_id = types.InlineKeyboardButton(text='Посмотреть свой id', callback_data='my_id')
            kb.add(my_id)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Выберите тему.',
                                  reply_markup=kb)

    """ Посмотреть id для ученика """
    if callback.data == 'my_id':
        prt = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton(text='Назад', callback_data='back')
        prt.add(back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text=f'Ваш id, чтобы передать родителю. {callback.message.chat.id}',
                              reply_markup=prt)



    """ Меню с выбором раздела по теме """
    for i in range(len(theme_titles) + 1):
        if callback.data == f'theme_s{i}':
            back__ = 0
            if back_track == 0:
                back_track = i
            prt = types.InlineKeyboardMarkup(row_width=1)
            train = types.InlineKeyboardButton(text='ТРЕНАЖЕР', callback_data=f'train{i}')
            interest = types.InlineKeyboardButton(text='ИНТЕРЕСНЫЕ ФАКТЫ', callback_data='interest')
            theory = types.InlineKeyboardButton(text='ТЕОРИЯ', callback_data=f'theory{i}')
            tests = types.InlineKeyboardButton(text='ТЕСТЫ', callback_data=f'tests{i}')
            results = types.InlineKeyboardButton(text='РЕЗУЛЬТАТЫ', callback_data=f'results{i}')
            back = types.InlineKeyboardButton(text='Назад', callback_data='back')
            prt.add(train, interest, theory, tests, results, back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Выберите раздел.',
                                  reply_markup=prt)

    """ Ученик. Тренажер. Вкладка для выбора теста """
    for i in range(1, len(theme_titles) + 1):
        if callback.data == f'train{i}':
            test_by_theme = sql.session.query(sql.Test_name.title, sql.Test_name.id) \
                .join(sql.Theme).filter(sql.Theme.id == i)
            tests_titles = [i[0] for i in test_by_theme]
            tests_id = [i[1] for i in test_by_theme]
            sources = types.InlineKeyboardMarkup(row_width=1)
            sources.add(
                *[types.InlineKeyboardButton(text=title, callback_data=f'train_question{id}')
                  for title, id in zip(tests_titles, tests_id)])
            back = types.InlineKeyboardButton(text='Назад', callback_data='back')
            sources.add(back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Выберете пробный тест для прохождения.',
                                  reply_markup=sources)

    """Ученик. Тренажер. Вкладка для вопросов и ответов """
    for i in range(1, len(tests_) + 1):
        if callback.data == f'train_question{i}':
            test_id_special = i
            questions_by_test = sql.session.query(sql.Test_question.content, sql.Test_question.id) \
                .join(sql.Test_name).filter(sql.Test_name.id == i)
            questions_by_test_ = [i[0] for i in questions_by_test]
            questions_by_test_id = [i[1] for i in questions_by_test]
            text = f'Можете попрактиковаться:\n'

            for question, id in zip(questions_by_test_, questions_by_test_id):
                answers_by_test = sql.session.query(sql.Test_answer.content, sql.Test_answer.right) \
                    .join(sql.Test_question, sql.Test_question.id == sql.Test_answer.test_q_id) \
                    .filter(sql.Test_answer.test_q_id == id)
                answers_by_test_ = [j[0] for j in answers_by_test]
                answers_by_test_isright = [j[1] for j in answers_by_test]
                right_answer_id = answers_by_test_isright.index(1)
                bot.send_poll(callback.message.chat.id, question, answers_by_test_,
                              type='quiz', correct_option_id=right_answer_id)

            sources = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(text='Назад', callback_data='back')
            sources.add(back)
            bot.send_message(callback.message.chat.id, text, reply_markup=sources)


        """ Вкладка с интересными фактами """
    if callback.data == f'interest':
        interest_content_ = [i[0] for i in sql.session.query(sql.Interesting.content)]
        sources = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton(text='Назад', callback_data='training_back')
        sources.add(back)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text='Интересные факты.')
        text = interest_content_[randint(0, len(interest_content_) - 1)]
        bot.send_message(chat_id=callback.message.chat.id, text=text,
                         reply_markup=sources)

        """ Вкладка с теорией """
    for i in range(len(theory_titles) + 1):
        if callback.data == f'theory{i}':
            theory_titles_ = [i[0] for i in sql.session.query(sql.Theory.title).filter(sql.Theory.theme_id == i)]
            theory_content_ = [i[0] for i in sql.session.query(sql.Theory.content).filter(sql.Theory.theme_id == i)]
            sources = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(text='Назад', callback_data='back')
            sources.add(*[types.InlineKeyboardButton(text=title, url=content) for title, content in zip(
                theory_titles_, theory_content_
            )])
            sources.add(back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Ознакомтесь с источниками.',
                                  reply_markup=sources)

        """ Раздел для просмотра результатов """
    for i in range(len(results_) + 1):
        if callback.data == f'results{i}':
            result = sql.session.query(sql.Result.result, sql.Test_name.title).join(sql.Test_name) \
                .join(sql.Theme).filter(sql.Theme.id == i, sql.Result.student_id == callback.message.chat.id)
            result_value = [i[0] for i in result]
            result_name = [i[1] for i in result]
            sources = types.InlineKeyboardMarkup(row_width=1)
            text = 'Ознакомтесь с результатами:\n'
            for v, n in zip(result_value, result_name):
                text += f'За тест {n} набранно {v} баллов.\n'
                # sources.add(types.InlineKeyboardButton(text=text))
            back = types.InlineKeyboardButton(text='Назад', callback_data='back')
            sources.add(back)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                  reply_markup=sources)

    """ Вкладка для выбора теста """
    for i in range(len(tests_) + 1):
        if callback.data == f'tests{i}':
            if back__ == 0:
                back__ = i
            test_by_theme = sql.session.query(sql.Test_name.title, sql.Test_name.id) \
                .join(sql.Theme).filter(sql.Theme.id == i)
            tests_titles = [i[0] for i in test_by_theme]
            tests_id = [i[1] for i in test_by_theme]
            sources = types.InlineKeyboardMarkup(row_width=1)
            sources.add(
                *[types.InlineKeyboardButton(text=title, callback_data=f'question{id}')
                  for title, id in zip(tests_titles, tests_id)])
            back = types.InlineKeyboardButton(text='Назад в главное меню', callback_data='back')
            back_s = types.InlineKeyboardButton(text='Назад', callback_data=f'theme_s{back_track}')
            sources.add(back, back_s)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                  text='Выберете тест для прохождения.',
                                  reply_markup=sources)

    """ Вкладка для вопросов и ответов """
    for i in range(len(tests_) + 1):
        if callback.data == f'question{i}':
            test_id_special = i
            questions_by_test = sql.session.query(sql.Test_question.content, sql.Test_question.id) \
                .join(sql.Test_name).filter(sql.Test_name.id == i)
            questions_by_test_ = [i[0] for i in questions_by_test]
            questions_by_test_id = [i[1] for i in questions_by_test]
            text = f'Выберите правильные ответы на вопросы:\n'
            poll_count = 0

            for question, id in zip(questions_by_test_, questions_by_test_id):
                poll_count = +1
                answers_by_test = sql.session.query(sql.Test_answer.content, sql.Test_answer.right) \
                    .join(sql.Test_question, sql.Test_question.id == sql.Test_answer.test_q_id) \
                    .filter(sql.Test_answer.test_q_id == id)
                answers_by_test_ = [j[0] for j in answers_by_test]
                answers_by_test_isright = [j[1] for j in answers_by_test]
                right_answer_id = answers_by_test_isright.index(1)
                bot.send_poll(callback.message.chat.id, question, answers_by_test_, is_anonymous=False,
                              type='quiz', correct_option_id=right_answer_id)

                @bot.poll_answer_handler(func=lambda callback: True)
                def handle_poll_answer(pollAnswer):
                    global answer_counter, student_result, test_id_special
                    # bot.send_message(callback.message.chat.id, text=f'Текст {pollAnswer.poll_id}')
                    user_answer_id = pollAnswer.option_ids[0]
                    if user_answer_id == right_answer_id:
                        answer_counter += 1

                    student_result = sql.Result(result=answer_counter, test_id=test_id_special,
                                                student_id=callback.message.chat.id)

            sources = types.InlineKeyboardMarkup(row_width=1)
            back = types.InlineKeyboardButton(text='Назад в главное меню', callback_data='back')
            back_s = types.InlineKeyboardButton(text='Назад', callback_data=f'tests{back__}')
            send_results = types.InlineKeyboardButton(text='Отправить результаты', callback_data='send_results')
            sources.add(send_results, back, back_s)
            bot.send_message(callback.message.chat.id, text, reply_markup=sources)

    if callback.data == 'send_results':
            sql.session.add(student_result)
            sql.session.commit()
            answer_counter = 0
            bot.send_message(callback.message.chat.id, text='Результаты отправлены')


bot.polling()