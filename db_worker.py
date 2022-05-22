import sqlite3

conn = sqlite3.connect('bot_db', check_same_thread=False, isolation_level=None)
cursor = conn.cursor()

create_table_classes = '''CREATE TABLE classes (
                       id INTEGER PRIMARY KEY,
                       title TEXT NOT NULL);'''
create_table_themes = '''CREATE TABLE themes (
                       id INTEGER PRIMARY KEY,
                       title TEXT NOT NULL);'''
create_table_theory = '''CREATE TABLE theory (
                       id INTEGER PRIMARY KEY,
                       title TEXT NOT NULL,
                       content TEXT NOT NULL,
                       theme_id INTEGER NOT NULL,
                       FOREIGN KEY (theme_id)
                        REFERENCES themes (id));'''
insert_classes = '''INSERT INTO classes (id, title)
                    VALUES (1, "Шестой класс"),
                    (2, "Седьмой класс"),
                    (3, "Восьмой класс"),
                    (4, "Девятый класс");'''
insert_themes = '''INSERT INTO themes (id, title)
                    VALUES (1, "ЛЕКСИКА"),
                    (2, "СЛОВООБРАЗОВАНИЕ"),
                    (3, "ОРФОГРАФИЯ"),
                    (4, "ЧАСТИ РЕЧИ");'''
insert_theory = '''INSERT INTO theory (id, title, content, theme_id)
                    VALUES (1, "Лексика как раздел языкознания","https://www.yaklass.ru/p/russky-yazik/10-klass/leksika-kak-razdel-iazykoznaniia-10519/passivnaia-leksika-10682", 1),
                    (2, "Способы словообразования","https://russkiiyazyk.ru/slovoobrazovanie/sposoby-slovoobrazovaniia.html", 2),
                    (3, "Орфография в таблицах","https://grammatika-rus.ru/glavnaya/orfograficheskij-razbor/orfografiya-v-tablitsah/", 3),
                    (4, "Части речи","https://russkiiyazyk.ru/chasti-rechi/chasti-rechi.html", 4);'''

""""
Блок команд для создания таблиц в нашей БД
и заполнения базовыми данными

cursor.execute(create_table_classes)
cursor.execute(create_table_themes)
cursor.execute(create_table_theory)
cursor.execute(insert_classes)
cursor.execute(insert_themes)
cursor.execute(insert_theory)

Используем только при первичном создании БД,
поскольку в SQLite нет поддержки блока
IF NOT EXISTS при создании таблиц

"""
grades = conn.execute('''SELECT title FROM classes''').fetchall()
grades = [grades[i][0] for i in range(len(grades))]
themes = conn.execute('''SELECT title FROM themes''').fetchall()
themes = [themes[i][0] for i in range(len(themes))]
theory = conn.execute('''SELECT title, content FROM theory''').fetchall()
theory_dict = [{theory[i][0]: theory[i][1]} for i in range(len(theory))]
theory_list = [(theory[i][0], theory[i][1]) for i in range(len(theory))]
theory_titles = [theory[i][0] for i in range(len(theory))]
theory_content = [theory[i][1] for i in range(len(theory))]
# for k,v in zip(theory_titles, theory_content): # Эта ерунда для проверки работы функции zip
#     print(k)
#     print(v)
# for i in theory_dict: # Эта ерунда просто для проверки того, как работает словарь theory_dict
#     for k in i:
#         print(k)
#         print(i[k])


