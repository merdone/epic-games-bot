import logging
import asyncio
from aiogram.enums import ParseMode

from app.parser_service import parser_loop
from app.loader import bot, dp
import app.bot.bot_handlers

logging.basicConfig(level=logging.INFO)


async def main():
    asyncio.create_task(parser_loop())
    await dp.start_polling(bot, parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was interrupted")
