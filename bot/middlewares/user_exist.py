from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.db.api import get_user, create_user
from bot.db.models.users import User


class UserMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_id = event.from_user.id

        user = await get_user(user_id)

        if user is None:

            user = User(
                tg_id=user_id,
                username=event.from_user.username if event.from_user.username else "",
                name=event.from_user.first_name
            )
            await create_user(user)

        data['user'] = user
        # print(2)
        return await handler(event, data)
