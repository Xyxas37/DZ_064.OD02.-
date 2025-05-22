import asyncio
import requests
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


def get_random_apod():
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        random_date = start_date + (end_date - start_date) * random.random()
        date_str = random_date.strftime("%Y-%m-%d")

        url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при запросе к NASA API: {e}")
        return {}


@dp.message(Command("random_apod"))
async def random_apod(message: Message):
    apod = get_random_apod()
    if not apod:
        await message.answer("Не удалось получить данные от NASA.")
        return

    media_url = apod.get("url")
    title = apod.get("title", "Без названия")
    media_type = apod.get("media_type")

    if media_type == "image":
        await message.answer_photo(photo=media_url, caption=title)
    elif media_type == "video":
        await message.answer(f"🎥 {title}\n{media_url}")
    else:
        await message.answer("Не удалось получить изображение или видео.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
