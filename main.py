import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

API_TOKEN = "7436967595:AAG1pMyNz0hoU2Owz4ENv9GkFU9742E8IV4"

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@dp.message(Command(commands=["start", "join"]))
async def join_handler(message: Message):
    users = load_users()
    if message.from_user.id not in users:
        users.append(message.from_user.id)
        save_users(users)
        await message.answer("Ты добавлен в список упоминаний!")
    else:
        await message.answer("Ты уже в списке.")

@dp.message()
async def mention_if_all_trigger(message: Message):
    if "@all" in message.text:
        users = load_users()
        if users:
            mentions = [f"[всех](tg://user?id={uid})" for uid in users]
            await message.answer("Важно, " + " ".join(mentions) + " отметил")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
