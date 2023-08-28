#Импорт библиотек
import os
import time
from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram import filters
from loguru import logger
from datetime import date
from dotenv import load_dotenv


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemy_base import User, Base

load_dotenv()
API_ID = os.getenv("api_id")
API_HASH = os.getenv("api_hash")
# api_id = 27045678
# api_hash = 'ce72c2c8198d70f546951aed037337ca'


client = Client(name='me_client', api_id=API_ID, api_hash=API_HASH)

engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3306/time_bot", echo=True)

session = sessionmaker(bind=engine)
s = session()

#создание файла с info.log и задание формата
logger.add("info.log", format="{time} {level} {message}",
           level="INFO", rotation="5 KB", compression="zip")

#функция(хендлер) команды /users_today
def command_start(client: Client, message: Message):
    list_user = []
    for row in s.query(User.id_tg, User.date_reg).distinct():
        if row[1] == date.today():
            list_user.append(row[0])

    client.send_message('me', f"Пользователи, которые зарегистрировались {date.today()}:")
    if list_user == []:
        client.send_message('me', "Нет пользователей")
        logger.info("Отправлен пустой список пользователей(info)")
    else:
        #отправка сообщения в чат "Избранное"
        client.send_message('me', "\n".join(map(str, list_user)))
        logger.info("Отправлен список пользователей(info)")

#функция(хендлер) все сообщения боту
def all_message(client: Client, message: Message):
    id_ch = str(message.chat.id)
    if id_ch[0] != '-':
        list_id = []
        for id in s.query(User.id_tg).distinct():
            list_id.append(id[0])


        #добавление проверка на наличие пользователя в БД и добавление
        if str(message.chat.id) in list_id:
            print('Уже есть в БД')
        else:
            id_us = User(id_tg=message.chat.id, date_reg=date.today())
            s.add(id_us)
            s.commit()
            print('Добавил')

        #отправка сообщения "Добрый день!" через 10мин
        time.sleep(600)
        client.send_message(id_ch, 'Добрый день!')
        logger.info("Добрый день!(info)")

        #отправка сообщения "Подготовила для вас материал" через 90мин
        time.sleep(5400)
        client.send_message(id_ch, 'Подготовила для вас материал')
        logger.info("Подготовил материал(info)")

        #отправка фото сразу после "Подготовила для вас материал"
        client.send_photo(id_ch, 'https://w.forfun.com/fetch/f1/f1ea8ae2e3a05e675f937fc177626474.jpeg')
        logger.info("Отправил фото(info)")

        # проверка на наличие в чате сообщения "Хорошего дня"
        if client.search_messages_count(id_ch, "Хорошего дня", from_user=message.from_user.id)==0:
            time.sleep(7200)
            client.send_message(id_ch, 'Скоро вернусь с новым материалом!')
            logger.info("Скоро вернусь(info)")


#регистрация хендлеров
client.add_handler(MessageHandler(command_start, filters.command('users_today')))
client.add_handler(MessageHandler(all_message, filters=(~filters.outgoing & ~filters.chat(chats='me'))))


client.run()
