import asyncio
from bot.bot_instance import bot, dp
from bot.services.gemini import setup_gemini
from bot.handlers import callbacks
from bot.handlers.user import cmd_start, cmd_random, handle_message

def register_handlers():
    dp.message.register(cmd_start)
    dp.message.register(cmd_random)
    dp.message.register(handle_message)
    dp.callback_query.register(callbacks.handle_more_button, lambda c: c.data == "more")

async def main():
    await setup_gemini()
    register_handlers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())