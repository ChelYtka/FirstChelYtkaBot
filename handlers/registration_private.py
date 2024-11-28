from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

#from db.users_db import cursor, connection
#from test_notice_bot import bot

from kbds import reply

from db.users_db import Database

database = Database()

#обработчик
registration_private_router = Router()

#class 


# хэндлер команды /start
@registration_private_router.message(lambda msg: msg.text == '/start')
async def process_start_cmd(message : Message, bot : Bot):
    user_id = message.from_user.id
    username = message.from_user.first_name
    # ищем юзера и запоминаем
    # подключаем базу данных
    db_user = await database.get_user(user_id)

    print(db_user)
    print(user_id)
    print(bot.admin_list)
    # если юзер нет
    if not db_user:
        if str(user_id) not in bot.admin_list:
            await message.answer\
            (
                f'Привет!\nРады приветствовать в нашем боте.\n'
                f'Чтобы узнать, как пользовиться ботом, '
                f'вводи команду /help',
                reply_markup=reply.get_keyboard\
                (
                    "Задачи",
                    "задача",
                    placeholder="список",
                    sizes=(1, 2)
                )   
            )
            # добавляем нового юзера
            await database.add_user(user_id, username, 'student')
            print(db_user)
            
        else:
            # добавляем нового админа
            await database.add_user(user_id, username, 'admin')
            await message.answer\
            (
                f'Привет!\nРады приветствовать нового админа.\n'
                f'Доступные команды можешь посмотреть в кнопках',
                reply_markup=reply.get_keyboard\
                (
                    "анигиляция",
                    "группы",
                    "активность",
                    placeholder="команды",
                    sizes=(2, )
                )   
            ) 
    else: # добавили новую кнопку в меню
        if str(user_id) not in bot.admin_list:
            await message.answer\
            (
                f'{username}, ты уже общаещься с ботом.\n'
                'Постарайся больше не вводить эту команду',
                reply_markup=reply.get_keyboard\
                (
                    "Задачи",
                    "задача",
                    placeholder="список",
                    sizes=(2,)
                ) 
            )
        else:
            await message.answer\
            (
                f'{username}, ты админ.\n'
                'Ныsе испытывай терпение бота.\n'
                'Можешь лишиться своих возможностей!!!',
                reply_markup=reply.get_keyboard\
                (
                    "анигиляция",
                    "группы",
                    "активность",
                    placeholder="команды",
                    sizes=(2, )
                )  
            )