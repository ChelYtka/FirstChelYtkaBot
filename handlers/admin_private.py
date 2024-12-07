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
admin_private_router.message.filter(ChatTypeFilter(['private']), IsAdmin())

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

class Delete(StatesGroup):
    group = State()

@admin_private_router.message(StateFilter(None), F.text == 'анигиляция')
async def process_delete_group(message : Message, state : FSMContext):
    await message.answer('Введите название группы')
    await state.set_state(Delete.group)

@admin_private_router.message(Delete.group)
async def process_search_group(message : Message, state : FSMContext):
    await state.update_data(group = message.text)
    group = await database.search_group(message.text.casefold())
    if group != None:
        await database.delete_group(group[1])
        await message.answer('Группа успешно удалена')
    else:
        await message.answer('Звиняй, не нашёл группу')
    await state.clear()

    
@admin_private_router.message(F.text == 'группы')
async def process_check_group(message : Message):
    groups = await database.return_groups()
    if groups != None:
        line = ''
        for group in groups:
            line += ('/n' + group[1])
        await message.answer(
            f'Вот список все групп:{line}'
        )
    else:
        await message.answer('Групп нет')   



@admin_private_router.message(F.text == 'активность')
async def process_delete_group(message : Message):
    active = await database.number()
    await message.answer(f'Всего в боте:\n'
                         f'\tПользователей - {active[0]}\n'
                         f'\tГрупп - {active[1]}')
