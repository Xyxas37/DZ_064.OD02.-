import os
import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY
from gtts import gTTS
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()
registered_users = set()

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('sound.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command("weather"))
async def weather(message: Message):
    city = "Moscow"
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(api_url)
        data = response.json()
        if data.get("main"):
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            await message.answer(f"🌦 Погода в {city}:\nТемпература: {temp}°C\nУсловия: {description}")
        else:
            await message.answer("❗Не удалось получить данные о погоде.")
    except Exception:
        await message.answer("Произошла ошибка при получении прогноза.")

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять '
        'творческие функции, которые традиционно считаются прерогативой человека; '
        'наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ'
    )

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды:\n"
        "/start — регистрация\n"
        "/help — помощь\n"
        "/myinfo — ваш Telegram ID\n"
        "/weather — прогноз погоды\n"
        "/photo — случайная картинка"
    )

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    registered_users.add(user_id)
    await message.answer(f"Приветики, я Бонд, Джеймс Бонд\n✅ Вы зарегистрированы!\nВаш Telegram ID: {user_id}")

@dp.message(F.photo)
async def save_all_photos(message: Message):
    list_responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list_responses)
    await message.answer(rand_answ)

    os.makedirs("img", exist_ok=True)
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_ext = file.file_path.split('.')[-1]
    file_path = f"img/{file_id}.{file_ext}"
    await bot.download(file, destination=file_path)

@dp.message(Command("myinfo"))
async def myinfo(message: Message):
    user_id = message.from_user.id
    if user_id in registered_users:
        await message.answer(f"🧾 Ваш Telegram ID: {user_id}")
    else:
        await message.answer("❗Вы не зарегистрированы. Нажмите /start.")

@dp.message(Command('photo'))
async def photo(message: Message):
    list_responses = [
        'https://techoparasol.es/static/main/img/solar-farm.webp',
        'https://techoparasol.es/media/blog_images/Paneles_Solares_y_Almacenamiento_Espa%C3%B1a.webp',
        'https://techoparasol.es/media/blog_images/energia-solar-ley-espana_U82yUtP.webp'
    ]
    rand_photo = random.choice(list_responses)
    await message.answer_photo(photo=rand_photo, caption='это хорошая картинка')

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1: \n1. Скручивания: 3 подхода по 15 повторений \n2. Велосипед: 3 подхода по 20 повторений (каждая сторона) \n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2: \n1. Подъемы ног: 3 подхода по 15 повторений \n2. Русский твист: 3 подхода по 20 повторений (каждая сторона) \n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3: \n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений \n2. Горизонтальные ножницы: 3 подхода по 20 повторений \n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")
    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile('training.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove("training.ogg")

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sound.ogg")
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("TG02.pdf")
    await bot.send_document(chat_id=message.chat.id, document=doc)

@dp.message(Command("say"))
async def say(message: Message):
    text = "Привет, это голосовое сообщение из бота!"
    tts = gTTS(text=text, lang='ru')
    tts.save("say.ogg")
    audio = FSInputFile("say.ogg")
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    os.remove("say.ogg")

@dp.message(F.text)
async def translate_to_english(message: Message):
    translator = Translator()
    translated = translator.translate(message.text, dest='en')
    await message.answer(f"Перевод на английский:\n{translated.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
