from app.database import Database
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
CHECK_INTERVAL = int(getenv("CHECK_INTERVAL"))
epic_url = str(getenv("epic_url"))
DB_NAME = getenv("DB_NAME")
if DB_NAME:
    db = Database(DB_NAME + ".db")
else:
    db = Database()

dp = Dispatcher()
