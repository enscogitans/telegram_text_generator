from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import defaultdict


# Родительский класс запсиси
Base = declarative_base()


# Класс нашей записи
class Record(Base):
    __tablename__ = 'model'

    chat_id = Column(String, primary_key=True)
    token_0 = Column(String, primary_key=True)
    token_1 = Column(String, primary_key=True)
    num = Column(Integer, default=1)

    def __repr__(self):
        return "<Record(chat_id={}, token_0={}, token_1={}, num={})>".format(
            self.chat_id, self.token_0, self.token_1, self.num)


# Подключение к нашей базе данных
engine = create_engine('sqlite:///model.db', echo=0)
Session = sessionmaker(bind=engine)
session = Session()


# Функция создание базы данных
def create_database():
    Base.metadata.create_all(engine)


# Функция добавления записи в таблицу. Возвращает True, если запись была создана,
# False, если такая запись уже существует
def try_add_record(chat_id, token_0, token_1, num=1):
    session.add(Record(chat_id=chat_id, token_0=token_0, token_1=token_1, num=num))

    try:
        session.commit()
        return True
    except IntegrityError:  # Если запись существует, отмена коммита
        session.rollback()
        return False


# Функция изменения в записи поля 'num'. Возвращает True, если запись была изменена,
# False, если записи не существует
def try_set_num(chat_id, token_0, token_1, new_num):
    try:
        record = session.query(Record).filter_by(chat_id=chat_id,
                                                 token_0=token_0,
                                                 token_1=token_1).one()
    except NoResultFound:   # Если такой записи нет, вернуть False
        return False

    record.num = new_num

    session.commit()
    return True


# Функция прибавления числа к полю 'num'. Возвращает True, если запись была изменена,
# False, если записи не существует
def try_increase_num(chat_id, token_0, token_1, add_to_num):
    try:
        record = session.query(Record).filter_by(chat_id=chat_id,
                                                 token_0=token_0,
                                                 token_1=token_1).one()
    except NoResultFound:   # Если такой записи нет, вернуть False
        return False

    record.num += add_to_num

    session.commit()
    return True


# Функция, возвращающая сумму всех num для конкретного чата
def get_sum_of_nums_for_token_in_chat(token, chat_id):
    return session.query(func.sum(Record.num)).filter_by(chat_id=chat_id,
                                                         token_0=token).one()[0]


# Функция, возвращающая словари с токенами и количеством их встречаний.
def get_tokens_and_nums_for_chat(chat_id):
    #
    lines = session.query(Record.token_0,
                          Record.token_1,
                          Record.num).filter_by(chat_id=chat_id).all()

    tokens = defaultdict(list)
    nums = defaultdict(list)

    for line in lines:
        tokens[line[0]].append(line[1])
        nums[line[0]].append(line[2])

    return tokens, nums
