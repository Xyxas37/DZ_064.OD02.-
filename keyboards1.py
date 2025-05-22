from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def greeting_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
        ],
        resize_keyboard=True
    )

def links_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://mapcasinoworld.com/")],
        [InlineKeyboardButton(text="Музыка", url="https://techoparasol.es/")],
        [InlineKeyboardButton(text="Видео", url="https://moybukhgalter.ru/")]
    ])

def dynamic_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="more")]
    ])

def more_options_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option2")]
    ])
