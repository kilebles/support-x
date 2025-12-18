import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.settings import TOKEN
from app.handlers import router, set_commands


async def main():
    bot = Bot(
        token=TOKEN, 
        default=DefaultBotProperties(parse_mode='HTML')
    )
    
    dp = Dispatcher()
    dp.include_router(router)

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
