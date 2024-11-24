from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

#from db.users_db import cursor, connection

from kbds import reply

from db.users_db import Database

database = Database()

#обработчик
user_private_router = Router()


# хэндлер команды /start
@user_private_router.message(lambda msg: msg.text == '/start')
async def process_start_cmd(message : Message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    # ищем юзера и запоминаем
    # подключаем базу данных
    db_user = await database.get_user(user_id)

    print(db_user)
    # если юзер нет
    if not db_user:
        await message.answer(
            f'Привет!\nРады приветствовать в нашем боте.\n'
            f'Чтобы узнать, как пользовиться ботом, '
            f'вводи команду /help',
            reply_markup=reply.start_kb   
        )
        
        await database.add_user(user_id, username, 'student')
        print(await database.get_user(user_id))
    else:
        await message.answer(
            f'{username}, ты уже общаещься с ботом.\n'
            'Постарайся больше не вводить эту команду',
            reply_markup=reply.start_kb  
        )


@user_private_router.message(lambda msg: msg.text == '/admin')
async def process_adm_cmd(message : Message):
    pass
    



@user_private_router.message(F.photo)
async def photo_message(message : Message):
    await message.reply('Это пхото')
