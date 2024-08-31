from aiogram import Bot, Dispatcher, types

import asyncio

from aiogram.client.default import DefaultBotProperties

from bot.settings import settings
from bot.middlewares import register_all_middlewares
from bot.routers import register_all_routers
from bot.settings import BOT_SCHEDULER
from bot.db.api import update_count_posts
from bot.logging import setup


async def main():

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True))
    dp = Dispatcher()

    register_all_routers(dp)
    register_all_middlewares(dp)
    BOT_SCHEDULER.add_job(update_count_posts, "cron", hour=0)
    BOT_SCHEDULER.start()
    await setup()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())