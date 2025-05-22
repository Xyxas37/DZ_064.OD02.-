import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN
import keyboards1 as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'Здравствуй, {message.from_user.first_name}, выбери вариант:',
        reply_markup=kb.greeting_keyboard()
    )

@dp.message(F.text == "Привет")
async def hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(F.text == "Пока")
async def bye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

@dp.message(Command("links"))
async def links(message: Message):
    await message.answer(
        "Выберите ссылку:",
        reply_markup=kb.links_keyboard()
    )


@dp.message(Command("dynamic"))
async def dynamic(message: Message):
    await message.answer(
        "Нажмите кнопку ниже:",
        reply_markup=kb.dynamic_keyboard()
    )

@dp.callback_query(F.data == "more")
async def show_more_options(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите опцию:",
        reply_markup=kb.more_options_keyboard()
    )

@dp.callback_query(F.data.in_({"option1", "option2"}))
async def handle_option(callback: CallbackQuery):
    option_text = "Опция 1" if callback.data == "option1" else "Опция 2"
    await callback.answer()
    await callback.message.answer(f"Вы выбрали: {option_text}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
