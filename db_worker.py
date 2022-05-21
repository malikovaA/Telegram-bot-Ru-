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
                       content TEXT NOT NULL,
                       theme_id INTEGER NOT NULL,
                       FOREIGN KEY (theme_id)
                        REFERENCES themes (id));'''
insert_classes = '''INSERT INTO classes (id, title)
                    VALUES (1, "Шестой"),
                    (2, "Седьмой"),
                    (3, "Восьмой"),
                    (4, "Девятый");'''
insert_themes = '''INSERT INTO themes (id, title)
                    VALUES (1, "ЛЕКСИКА"),
                    (2, "СЛОВООБРАЗОВАНИЕ"),
                    (3, "ОРФОГРАФИЯ"),
                    (4, "ЧАСТИ РЕЧИ");'''
insert_theory = '''INSERT INTO theory (id, content, theme_id)
                    VALUES (1, "https://www.yaklass.ru/p/russky-yazik/10-klass/leksika-kak-razdel-iazykoznaniia-10519/passivnaia-leksika-10682", 1),
                    (2, "https://russkiiyazyk.ru/slovoobrazovanie/sposoby-slovoobrazovaniia.html", 2),
                    (3, "https://grammatika-rus.ru/glavnaya/orfograficheskij-razbor/orfografiya-v-tablitsah/", 3),
                    (4, "https://russkiiyazyk.ru/chasti-rechi/chasti-rechi.html", 4);'''

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

