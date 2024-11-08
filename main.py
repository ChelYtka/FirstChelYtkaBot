from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart # Command - фильтрует апдейты на наличие новых /команд
from aiogram.types import Message
import random

f = open('token.txt')
BOT_TOKEN = f.readline()# токен бота

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# кол-во попыток пользователя
ATTEMPTS = 7
MIN_GAME_NUMBER = 1
MAX_GAME_NUMBER = 100

# словарь для хранения пользователей
users = {}
# словарь для хранения данных в случае одного пользователя 
'''user =  {
            'in_game' : False,
            'secret_number' : None,
            'attempts' : None,
            'total_games' : 0,
            'wins' : 0
        }
'''

# возвращает случайное число
def get_random_number() -> int:
    return random.randint(MIN_GAME_NUMBER, MAX_GAME_NUMBER)

# хэндлер команды /start
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду\n/help'
    )
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }


# хэндлер команды /help
@dp.message(Command(commands = 'help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от {MIN_GAME_NUMBER} до {MAX_GAME_NUMBER},'
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS}'
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancle - выйти из игры'
        f'\n/stat - посмотреть статистику\n\nДавай сыграем?'
        )
    
# хэндлер команды /stat
@dp.message(Command(commands = 'stat'))
async def process_stat_command(message : Message):
    await message.answer(
            f'Всего игр сыграно: '
            f'{users[message.from_user.id]["total_games"]}\n'
            f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )

# хэндлер команды /cancle
@dp.message(Command(commands = 'cancle'))
async def process_cancle_command(message : Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            f'Вы вышли из игры. Если хотите сыграть '
            f'снова - напишите об этом'
        )
    else:
        await message.answer(
            f'А мы и так с вами не играем. '
            f'Может, сыграем разок?'
        )

# хэндлер срабатывающий на согласие пользоватаеля сыграть
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            f'Ура!\n\nЯ загадал число от {MIN_GAME_NUMBER} до {MAX_GAME_NUMBER}, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            f'реагировать только на числа от {MIN_GAME_NUMBER} до {MAX_GAME_NUMBER} '
            'и команды /cancel и /stat'
        )

# хэндлер срабатывающий на отказ пользователя сыграть
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message : Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто)'
            'напишите об этом'
        )
    else: 
        await message.answer(
            'Мы уже сейчас с вами играем. Посылайте, '
            f'пожалуйста, числа от {MIN_GAME_NUMBER} до {MAX_GAME_NUMBER}'
        )

# хэндлер срабатывающий на отправку числа
@dp.message(lambda x:   x.text and x.text.isdigit()
                        and MIN_GAME_NUMBER<=int(x.text) <= MAX_GAME_NUMBER)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}'
                f'\n\nДавайте сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# хэндлкр срабатывающий на остальные сообщения
@dp.message()
async def process_other_answers(message: Message):
    # добавление нового пользователя
    if message.from_user.id not in users:
        await message.answer(
            'Для начала работы с ботом '
            'введите команду /start '
        )
    else:
        if users[message.from_user.id]['in_game']:
            await message.answer(
                'Мы же сейчас с вами играем. '
                f'Присылайте, пожалуйста, числа от {MIN_GAME_NUMBER} до {MAX_GAME_NUMBER}'
            )
        else:
            await message.answer(
                'Я довольно ограниченный бот, давайте '
                'просто сыграем в игру?'
            )
    

if __name__ == '__main__':
    dp.run_polling(bot)