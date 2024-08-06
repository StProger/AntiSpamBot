from aiogram import Dispatcher

from bot.middlewares.user_exist import UserMiddleware
from bot.middlewares.throttling import ThrottlinkMiddleware


def register_all_middlewares(dp: Dispatcher):

    dp.message.outer_middleware(UserMiddleware())
    dp.message.middleware(ThrottlinkMiddleware())