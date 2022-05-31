from sqlalchemy import  create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

engine = create_engine('sqlite:///bot_db?check_same_thread=False')
cursor = engine.connect()
session = Session(bind=engine)

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

class Theme(Base):
    __tablename__ = 'themes'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    tests = relationship('Test_name', backref='theme')

class Test_name(Base):
    __tablename__ = 'test_names'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id'))

test1 = Test_name(title='TEST NAME', theme_id=1)

class Test_question(Base):
    __tablename__ = 'test_questions'
    id = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=False)
    test_id = Column(Integer, ForeignKey('test_names.id'))
    test_name = relationship('Test_name', backref='questions')

question1 = Test_question(content='Bla bla bla question', test_id=1)

class Test_answer(Base):
    __tablename__ = 'test_answer'
    id = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=False)
    right = Column(Integer, nullable=False, default=0)
    test_q_id = Column(Integer, ForeignKey('test_questions.id'))
    question = relationship('Test_question', backref='answers')

answer1 = Test_answer(content='Answer1', test_q_id=1)
answer2 = Test_answer(content='Answer2', right=1, test_q_id=1)

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    result = Column(Integer, nullable=False)
    test_id = Column(Integer, ForeignKey('test_names.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship('Student', backref='results')
    test_name = relationship('Test_name', backref='results')

class Theory(Base):
    __tablename__ = 'theory'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(100), nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id'))
    theme = relationship('Theme', backref='theory')

# Base.metadata.drop_all(engine) # Удаление всего
# Base.metadata.create_all(engine)

c6 = Class(title='Шестой класс')
c7 = Class(title='Седьмой класс')
c8 = Class(title='Восьмой класс')
c9 = Class(title='Девятый класс')

t1 = Theme(title='ЛЕКСИКА')
t2 = Theme(title='СЛОВООБРАЗОВАНИЕ')
t3 = Theme(title='ОРФОГРАФИЯ')
t4 = Theme(title='ЧАСТИ РЕЧИ')

tt1 = Theory(title='Лексика как раздел языкознания',content='https://www.yaklass.ru/p/russky-yazik/10-klass/leksika-kak-razdel-iazykoznaniia-10519/passivnaia-leksika-10682',theme_id=1)
tt2 = Theory(title='Способы словообразования',content='https://russkiiyazyk.ru/slovoobrazovanie/sposoby-slovoobrazovaniia.html',theme_id=2)
tt3 = Theory(title='Орфография в таблицах',content='https://grammatika-rus.ru/glavnaya/orfograficheskij-razbor/orfografiya-v-tablitsah/',theme_id=3)
tt4 = Theory(title='Части речи',content='https://russkiiyazyk.ru/chasti-rechi/chasti-rechi.html',theme_id=4)

# session.add_all([c6,c7,c8,c9,t1,t2,t3,t4,t1,tt1,tt2,tt3,tt4, test1, question1, answer1, answer2])
# result = Result(result=7, test_id=1, student_id=319570020)
# session.add(result)
# session.commit()

# for i in range(1,5):
#     session.add(Student(name=f'Denis Petrov{i}', class_id=i))
# session.commit()
