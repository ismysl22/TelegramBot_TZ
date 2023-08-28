from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from pathlib import Path

# подключение к бд
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
DB_NAME = BASE_DIR / "users.db"
engine = create_engine(f"sqlite:///{str(DB_NAME)}")

Base = declarative_base()


class User(Base):
     __tablename__ = 'Users'
     # создание таблиц
     id_user = Column(Integer, primary_key=True)
     id_tg = Column(String(250), nullable=False)
     date_reg = Column(Date, nullable=False)


Base.metadata.create_all(engine)

