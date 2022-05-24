from sqlalch import Class, Student, Theme, Test_name, Test_answer, Test_question, Result, Theory
from openpyxl import load_workbook

# import telebot
# bot = telebot.TeleBot(token)
#


""" 
    Пока эта функция просто читает каждую строку файла Excel
    Идея - учитель записывает тест (вопросы и ответы)
    в правильном порядке в Excel файл и с помощью
    этой функции мы его парсим, а потом полученные
    данные записываем в БД в таблицы 
    Test_names, Test_questions, Test_answers   
"""

def import_test(doc_name):
    doc_name = 'test.xlsx'
    wb = load_workbook('files/'+doc_name)
    sheet = wb.active
    for row in sheet:
        print('row')
        for cell in row:
            print(cell.value)
