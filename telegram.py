from aiogram import Bot, types

async def send_telegram_message(api_token, chat_id, message):
    # create object bot
    bot = Bot(token=api_token)

    # send message
    await bot.send_message(chat_id, message)