from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from filters.chat_types import ChatTypeFilter, IsAdmin

#from db.users_db import cursor, connection
#from test_notice_bot import bot

from kbds import reply

from db.users_db import Database

database = Database()

#обработчик
admin_private_router = Router()
#admin_private_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

ADMIN_KB = reply.get_keyboard(
        'группы',
        'аннигиляция',
        'активность',
        placeholder='выберите действие',
        sizes=(2,1),
)
'''
Разработать функции доступные только для админа
группы
аннигиляция
активность
'''

@admin_private_router.message(F.text == 'админ')
async def process_admin_check(message : Message, bot : Bot):
    if message.from_user.id in bot.admin_list:
        await message.answer('Что вы хотели, мой господин?')

@admin_private_router.message(F.text == 'группы')
async def process_check_group(message : Message):
    pass