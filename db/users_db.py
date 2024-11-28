import aiosqlite



# класс для работы с бд
class Database:
    def __init__(self, db_name='bot_db.db'):
        # инициализируем класс
        self.db_name = r'db/'+db_name

    async def create_database(self):
        # создание бд и таблиц, если их нет

        # подключаемя к бд с проверкой на ошибки
        async with aiosqlite.connect(self.db_name) as db:
            # создаём users
            await db.execute('''
                            CREATE TABLE IF NOT EXISTS Users (
                             user_id INTEGER PRIMARY KEY,
                             telegram_id TEXT UNIQUE NOT NULL,
                             user_name TEXT NOT NULL,
                             role TEXT CHECK(role IN ('student', 
                             'headman', 'admin')) NOT NULL,
                             group_id INTEGER,
                             FOREIGN KEY(group_id) REFERENCES Groups(group_id)
                             )
                             ''')
            
            # создаём groups
            await db.execute('''
                            CREATE TABLE IF NOT EXISTS Groups(
                             group_id INTEGER PRIMARY KEY,
                             group_name TEXT NOT NULL,
                             headman_id INTEGER,
                             FOREIGN KEY (headman_id) REFERENCES Users(user_id)
                             )
                             ''')

            # Создаем assignments
            await db.execute('''
            CREATE TABLE IF NOT EXISTS Assignments (
                assignment_id INTEGER PRIMARY KEY,
                group_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                due_date DATE NOT NULL,
                description TEXT,
                created_by INTEGER NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES Groups(group_id),
                FOREIGN KEY (created_by) REFERENCES Users(user_id)
            )
            ''')

            # Создаем таблицу Tokens
            await db.execute('''
            CREATE TABLE IF NOT EXISTS Tokens (
                token_id INTEGER PRIMARY KEY,
                token TEXT UNIQUE NOT NULL,
                is_used BOOLEAN DEFAULT FALSE
            )
            ''')

            # Сохраняем изменения в базе данных
            await db.commit()

    # добавление юзера
    async def add_user(self, telegram_id, user_name, role, group_id=None):
        async with aiosqlite.connect(self.db_name) as db:
            try:
                await db.execute('''
                            INSERT INTO Users (telegram_id, user_name, role, group_id)
                             VALUES(?, ?, ?, ?)
                             ''', (str(telegram_id), user_name, role, group_id)
                             )
                await db.commit()
            except Exception as e:
                print(f"Error adding user: {e}")

    # получение инф-и о пользователе
    async def get_user(self, telegram_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute("SELECT * FROM Users WHERE telegram_id = ?",
                                      (str(telegram_id),))
            return await cursor.fetchone()
        

    async def get_admin(self, telegram_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute("SELECT * FROM Users WHERE telegram_id = ?", str(telegram_id),)
            return await cursor.fetchone()




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