import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'Здравствуй, {message.from_user.first_name}! Выбери континент:',
        reply_markup=await kb.continents_keyboard()
    )


@dp.callback_query(F.data.startswith("continent_"))
async def handle_continent(callback: CallbackQuery):
    continent_key = callback.data.split("_", 1)[1]
    await callback.message.edit_text(
        f"Вы выбрали континент: {continent_key.capitalize()}\nВыберите страну:",
        reply_markup=await kb.countries_keyboard(continent_key)
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("country_"))
async def handle_country(callback: CallbackQuery):
    country = callback.data.split("_", 1)[1].replace("_", " ").title()
    await callback.message.answer(f"Вы выбрали страну: {country}")
    await callback.answer()


@dp.callback_query(F.data == "back_to_continents")
async def back_to_continents(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите континент:",
        reply_markup=await kb.continents_keyboard()
    )
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
