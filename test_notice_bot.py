import asyncio
import os # для работы с операционкой


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, BotCommandScopeAllPrivateChats

# для работы с окружением
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from common.bot_cmds_list import private

BOT_TOKEN = os.getenv('TOKEN')# токен бота

# создаём бота и диспетчера
bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()



dp.include_router(user_private_router)
# Основная функция для запуска бота
async def main():
    try:
        # удалить меню
        #await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
        # создать меню
        await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
        # Запуск бота с использованием нового метода
        await dp.start_polling(bot)
    finally:
        # Закрытие соединения при завершении работы бота
        #connection.close()
        print("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    asyncio.run(main())