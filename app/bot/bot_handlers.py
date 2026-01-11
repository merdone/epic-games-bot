from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.loader import db, dp

from app.bot.bot_utils import send_game_card

subscribe_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Yes, send me games!", callback_data="sub_yes"),
        InlineKeyboardButton(text="❌ No, thanks", callback_data="sub_no")
    ]
])


@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if db.user_exists(user_id):
        await message.answer("You are already subscribed! Stay tuned for new giveaways.")
        return

    await message.answer(
        f"Hello, {user_name}! 👋\n\n"
        "I am a bot that tracks free giveaways on the Epic Games Store.\n"
        "Would you like me to notify you when a new free game becomes available?",
        reply_markup=subscribe_kb
    )


@dp.callback_query(F.data == "sub_yes")
async def process_subscribe(callback: CallbackQuery):
    user_id = callback.from_user.id

    db.add_user(user_id)

    await callback.message.edit_text(
        "✅ Subscription confirmed!\n"
        "Now you won't miss a single game."
    )

    active_games = db.get_active_games()

    if active_games:
        await callback.message.answer("🔥 Currently free:")

        for game in active_games:
            await send_game_card(callback.bot, callback.message.chat.id, game)

    else:
        await callback.message.answer(
            "Unfortunately, there are no active giveaways right now. But I'll let you know as soon as they appear!")
    await callback.answer()


@dp.callback_query(F.data == "sub_no")
async def process_decline(callback: CallbackQuery):
    await callback.message.edit_text(
        "Okay, I won't disturb you.\n"
        "If you change your mind — just press /start again."
    )
    await callback.answer()
