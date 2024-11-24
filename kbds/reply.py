from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



# записываем список списка кнопок
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="О нас"),
        ],
        [
            KeyboardButton(text="Посмотреть"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интерисует?'
)