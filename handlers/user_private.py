from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from db.users_db import cursor, connection

#обработчик
user_private_router = Router()



# хэндлер команды /start
@user_private_router.message(lambda msg: msg.text == '/start')
async def process_start_cmd(message : Message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    # ищем юзера и запоминаем
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, ))
    db_user = cursor.fetchone()
    print(db_user)
    # если юзер нет
    if not db_user:
        await message.answer(
            f'Привет!\nРады приветствовать в нашем боте.\n'
            f'Чтобы узнать, как пользовиться ботом, '
            f'вводи команду /help'    
        )
        
        cursor.execute('INSERT INTO users (user_id, username) \
                       VALUES (?, ?)', (user_id, username))   
        connection.commit()
    else:
        await message.answer(
            f'{username}, ты уже общаещься с ботом.\n'
            'Постарайся больше не вводить эту команду'
        )


@user_private_router.message(F.photo)
async def photo_message(message : Message):
    await message.reply('Это пхото')
