import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.db import Database

async def main():
    db = Database(path="bot.db")
    await db.create_users_table()
    await db.create_books_table()
    await db.create_order_table()
    
    bot = Bot(token='7721319298:AAEocrlZkQE_M8ow82Pq1nhcLMdnAbTVAe4')
    
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
