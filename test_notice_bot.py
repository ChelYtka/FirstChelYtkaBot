import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message


f = open('token.txt')
BOT_TOKEN = f.readline()# токен бота
f.close()

# создаём бота и диспетчера
bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()

# подключаем базу данных
connection = sqlite3.connect('users.db')
# создаём курсор
cursor = connection.cursor()
# создаём таблицу
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               user_id TEXT NOT NULL,
               username TEXT NOT NULL
               )
''')
# сохраняем изменения
connection.commit()

# добавление
# cursor.execute('INSERT INTO Users (user_id, username) 
#               VALUES (?, ?)', ('id телеги', 'first_name'))

# Удаляем пользователя(переделать для заметок)
# сursor.execute('DELETE FROM Users WHERE user_id = ?', ('id из телеги',))

''' извлечение данных
# Выбираем всех пользователей
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()

# Выводим результаты
for user in users:
    print(user)
'''
'''
Для получения информации там есть своя система фильтров
cur.execute("SELECT * FROM Users WHERE id = ?", (id, ))
all = cur.fetchone()
'''

# хэндлер команды /start
@dp.message(lambda msg: msg.text == '/start')
async def process_start_command(message : Message):
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

# Основная функция для запуска бота
async def main():
    try:
        # Запуск бота с использованием нового метода
        await dp.start_polling(bot)
    finally:
        # Закрытие соединения при завершении работы бота
        connection.close()
        print("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())