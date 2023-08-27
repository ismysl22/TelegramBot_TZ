from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# подключение к бд
engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3306/time_bot", echo=True)

Base = declarative_base()


class User(Base):
     __tablename__ = 'Users'
     # создание таблиц
     id_user = Column(Integer, primary_key=True)
     id_tg = Column(String(250), nullable=False)
     date_reg = Column(Date, nullable=False)


Base.metadata.create_all(engine)

