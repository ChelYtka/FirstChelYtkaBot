from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

#from db.users_db import cursor, connection
#from test_notice_bot import bot

from kbds import reply

from db.users_db import Database

database = Database()
user_private_router = Router()



@user_private_router.message(lambda msg: msg.text == '/admin')
async def process_adm_cmd(message : Message):
    pass
    



@user_private_router.message(F.photo)
async def photo_message(message : Message):
    await message.reply('Это пхото')
