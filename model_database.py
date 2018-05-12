from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
def try_add_record(chat_id, token_0, token_1):
    session.add(Record(chat_id=chat_id, token_0=token_0, token_1=token_1))

    try:
        session.commit()
        return True
    except IntegrityError:  # Если запись существует, отмена коммита
        session.rollback()
        return False


# Функция изменения в записи поля num. Возвращает True, если запись была изменена,
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
