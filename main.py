import time
import mysql.connector
from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from pyrogram import filters
from loguru import logger
from datetime import date

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from alchemy_base import User, Base
from pyrogram.types import BotCommand

api_id = 27045678
api_hash = 'ce72c2c8198d70f546951aed037337ca'

#bot_token = '6319380609:AAHcsbdyPYkXIKWF9uW4JTWE7hzumxaWD0s'

client = Client(name='me_client', api_id=api_id, api_hash=api_hash)

engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3306/time_bot", echo=True)

session = sessionmaker(bind=engine)
s = session()

# async def filter_text(_, __, message):
#     return message.text == '/start'
#
# filter_data = filters.create(filter_text)
#
# def message_start(client: Client, message: Message):
#     client.send_message(message.chat.id, 'Привет!')


# @client.on_message(filters.command('users_today'))
# def start_handler(client: Client, message: Message):

logger.add("info.log", format="{time} {level} {message}",
           level="INFO", rotation="10 KB", compression="zip")

def command_start(client: Client, message: Message):
    list_user = []
    for row in s.query(User.id_tg, User.date_reg).distinct():
        if row[1] == date.today():
            list_user.append(row[0])
    print(list_user)
    client.send_message('me', f"Пользователи, которые зарегистрировались {date.today()}:")
    if list_user == []:
        client.send_message('me', "Нет пользователей")
        logger.info("Отправлен пустой список пользователей(info)")
    else:
        client.send_message('me', "\n".join(map(str, list_user)))
        logger.info("Отправлен список пользователей(info)")

#@client.on_message()
def all_message(client: Client, message: Message):
    id_ch = str(message.chat.id)
    if id_ch[0] != '-':
        list_id = []
        for id in s.query(User.id_tg).distinct():
            list_id.append(id[0])

        print(list_id)

        if str(message.chat.id) in list_id:
            print('Уже есть в БД')
        else:
            id_us = User(id_tg=message.chat.id, date_reg=date.today())
            s.add(id_us)
            s.commit()
            print('Добавил')


        #client.send_chat_action(message.chat.id, ChatAction.TYPING)
        time.sleep(5)
        client.send_message(id_ch, 'Добрый день!')
        logger.info("Добрый день!(info)")

        time.sleep(10)
        client.send_message(id_ch, 'Подготовила для вас материал')
        logger.info("Подготовил материал(info)")
        client.send_photo(id_ch, 'https://w.forfun.com/fetch/f1/f1ea8ae2e3a05e675f937fc177626474.jpeg')
        logger.info("Отправил фото(info)")


        print(client.search_messages_count(id_ch, "Hi", from_user=1063818709))

        # message.reply('Test message')
        # message.copy('@i5my5I')
        # for message in client.search_messages(id_ch, 'Hi', from_user="me"):
        #     print(message.text)

        # if client.search_messages_count(id_ch, 'Hi', from_user="1063818709")==1:
        #     time.sleep(10)
        #     client.send_message(id_ch, 'Подготовила для вас материал')
        #     logger.info("Скоро вернусь(info)")





        #client.send_message('@i5my5I', 'Скоро вернусь с новым материалом!')

    # if client.search_messages('@i5my5I', 'Хорошего дня', 0, 'no filter', 1, from_user="timebot") == 'Хорошего дня':
    #     client.send_message('@i5my5I', 'Скоро вернусь с новым материалом!')


#client.add_handler(MessageHandler(message_start, filter_data))
#client.add_handler(MessageHandler(command_start, filters.command(commands='start')))

client.add_handler(MessageHandler(command_start, filters.command('users_today')))
client.add_handler(MessageHandler(all_message, filters=(~filters.outgoing & ~filters.chat(chats='me'))))


# bot_commands = [
#     BotCommand(
#         command='start',
#         description='Get started'
#     )
# ]


#client.add_handler(MessageHandler(all_message))
client.run()
# client.start()
# client.set_bot_commands(bot_commands)
# idle()
# client.stop()