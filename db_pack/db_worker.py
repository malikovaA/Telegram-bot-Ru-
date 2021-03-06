import sqlite3
from sqlalchemy import  create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# conn = sqlite3.connect('bot_db', check_same_thread=False, isolation_level=None)
# cursor = conn.cursor()

engine = create_engine('sqlite:///bot_db')
cursor = engine.connect()



Base = declarative_base()

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'))
    results = relationship('Result', backref='student')

class Theme(Base):
    __tablename__ = 'themes'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    tests = relationship('Test_name', backref='theme')
    theory = relationship('Theory', backref='theme')

class Test_name(Base):
    __tablename__ = 'test_names'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id'))
    questions = relationship('Test_questions', backref='test_name')
    results = relationship('Result', backref='test_name')

class Test_question(Base):
    __tablename__ = 'test_questions'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    test_id = Column(Integer, ForeignKey('test_names.id'))
    answers = relationship('Test_answer', backref='question')

class Test_answer(Base):
    __tablename__ = 'test_answer'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    right = Column(Integer, nullable=False)
    test_q_id = Column(Integer, ForeignKey('test_questions.id'))

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    result = Column(Integer, nullable=False)
    test_id = Column(Integer, ForeignKey('test_names.id'))
    student_id = Column(Integer, ForeignKey('students.id'))

class Theory(Base):
    __tablename__ = 'theory'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(100), nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id'))


create_table_classes = '''CREATE TABLE classes (
                       id INTEGER PRIMARY KEY,
                       title TEXT NOT NULL);'''
create_table_students = '''CREATE TABLE students (
                       id INTEGER PRIMARY KEY,
                       name TEXT NOT NULL,
                       class_id INTEGER NOT NULL,
                       FOREIGN KEY (class_id)
                        REFERENCES classes (id));'''
create_table_themes = '''CREATE TABLE themes (
                       id INTEGER PRIMARY KEY,
                       title TEXT NOT NULL);'''
create_table_test_names = '''CREATE TABLE test_names (
                       id INTEGER PRIMARY KEY,
                       title TEXT NOT NULL,
                       theme_id INTEGER NOT NULL,
                       FOREIGN KEY (theme_id)
                        REFERENCES themes (id));'''
create_table_test_questions = '''CREATE TABLE test_questions (
                       id INTEGER PRIMARY KEY,
                       content TEXT NOT NULL,
                       test_id INTEGER NOT NULL,
                       FOREIGN KEY (test_id)
                        REFERENCES test_names (id));'''
create_table_test_answers = '''CREATE TABLE test_answers (
                       id INTEGER PRIMARY KEY,
                       content TEXT NOT NULL,
                       right INTEGER NOT NULL,
                       test_q_id INTEGER NOT NULL,
                       FOREIGN KEY (test_q_id)
                        REFERENCES test_questions (id));'''
create_table_results = '''CREATE TABLE results (
                       id INTEGER PRIMARY KEY,
                       result INT NOT NULL,
                       test_id INTEGER NOT NULL,
                       student_id INTEGER NOT NULL,
                       FOREIGN KEY (test_id)
                        REFERENCES test_names (id),
                       FOREIGN KEY (student_id)
                        REFERENCES students (id));'''
create_table_theory = '''CREATE TABLE theory (
                       id INTEGER PRIMARY KEY,
                       title TEXT NOT NULL,
                       content TEXT NOT NULL,
                       theme_id INTEGER NOT NULL,
                       FOREIGN KEY (theme_id)
                        REFERENCES themes (id));'''
insert_classes = '''INSERT INTO classes (id, title)
                    VALUES (1, "???????????? ??????????"),
                    (2, "?????????????? ??????????"),
                    (3, "?????????????? ??????????"),
                    (4, "?????????????? ??????????");'''
insert_themes = '''INSERT INTO themes (id, title)
                    VALUES (1, "??????????????"),
                    (2, "????????????????????????????????"),
                    (3, "????????????????????"),
                    (4, "?????????? ????????");'''
insert_theory = '''INSERT INTO theory (id, title, content, theme_id)
                    VALUES (1, "?????????????? ?????? ???????????? ??????????????????????","https://www.yaklass.ru/p/russky-yazik/10-klass/leksika-kak-razdel-iazykoznaniia-10519/passivnaia-leksika-10682", 1),
                    (2, "?????????????? ????????????????????????????????","https://russkiiyazyk.ru/slovoobrazovanie/sposoby-slovoobrazovaniia.html", 2),
                    (3, "???????????????????? ?? ????????????????","https://grammatika-rus.ru/glavnaya/orfograficheskij-razbor/orfografiya-v-tablitsah/", 3),
                    (4, "?????????? ????????","https://russkiiyazyk.ru/chasti-rechi/chasti-rechi.html", 4);'''

""""
???????? ???????????? ?????? ???????????????? ???????????? ?? ?????????? ????
?? ???????????????????? ???????????????? ??????????????

cursor.execute(create_table_classes)
cursor.execute(create_table_themes)
cursor.execute(create_table_theory)
cursor.execute(create_table_test_names)
cursor.execute(create_table_test_questions)
cursor.execute(create_table_test_answers)
cursor.execute(create_table_results)
cursor.execute(insert_classes)
cursor.execute(insert_themes)
cursor.execute(insert_theory)

???????????????????? ???????????? ?????? ?????????????????? ???????????????? ????,
?????????????????? ?? SQLite ?????? ?????????????????? ??????????
IF NOT EXISTS ?????? ???????????????? ????????????

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


