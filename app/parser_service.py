from app.parsers.epicgames import EpicGamesParser
import asyncio
from app.bot.bot_utils import send_game_card
import logging

from app.loader import db, bot, CHECK_INTERVAL


async def parser_loop():
    parsers = [
        EpicGamesParser()
    ]
    while True:
        tasks = [parser.parse() for parser in parsers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for games in results:
            try:
                for game_info in games:

                    game_id = game_info['game_id']

                    if not db.game_exists(game_id):
                        db.add_game(game_info)

                        game_tuple = (
                            game_info['name'],
                            game_info.get('description', ''),
                            game_info['link'],
                            game_info.get('image_url'),
                            game_info.get('start_date'),
                            game_info.get('end_date')
                        )

                        users = db.get_active_users()
                        for user in users:
                            user_id = user[0]
                            await send_game_card(bot, user_id, game_tuple)
                        logging.info(f"Broadcast for {game_info['name']} finished.")

            except Exception as e:
                logging.error(f"Error in parser loop: {e}")
            await asyncio.sleep(CHECK_INTERVAL)
