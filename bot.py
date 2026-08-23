import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import search


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(search.router)

    # Удаление вебхуков перед long-polling
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот запущен и готов к обработке запросов...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
