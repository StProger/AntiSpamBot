from aiogram import Dispatcher

from bot.routers import antispam


def register_all_routers(dp: Dispatcher):

    dp.include_router(antispam.router)