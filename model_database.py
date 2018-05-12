from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String


Base = declarative_base()


class Model(Base):
    __tablename__ = 'model'

    chat_id = Column(String, primary_key=True)
    token_0 = Column(String, primary_key=True)
    token_1 = Column(String, primary_key=True)

    def __repr__(self):
        return "<Model(chat_id={}, token_0={}, token_1={})>".format(
            self.chat_id, self.token_0, self.token_1)
