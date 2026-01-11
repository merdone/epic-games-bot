from aiogram import Bot
from datetime import datetime
import logging


async def send_game_card(bot: Bot, chat_id: int, game_data: tuple):
    try:
        title = game_data[0]
        description = game_data[1]
        link = game_data[2]
        image_url = game_data[3]
        start_date = game_data[4]
        end_date = game_data[5]
        dt_start = datetime.fromisoformat(str(start_date).replace('Z', '+00:00')).strftime("%d-%m-%Y %H:%M")
        dt_end = datetime.fromisoformat(str(end_date).replace('Z', '+00:00')).strftime("%d-%m-%Y %H:%M")
        date_info = f"\n📅 Free from <b>{dt_start}</b> until: <b>{dt_end} </b>"

        caption = (
            f"🎮 <b>{title}</b>\n\n"
            f"{description}\n"
            f"{date_info}\n\n"
            f"👉 <a href='{link}'>Claim Game</a>"
        )

        if image_url:
            await bot.send_photo(
                chat_id=chat_id,
                photo=image_url,
                caption=caption,
                parse_mode="HTML"
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=caption,
                parse_mode="HTML",
                disable_web_page_preview=False
            )
    except Exception as e:
        logging.error(f"Error sending game to user {chat_id}: {e}")
