from sqlalchemy import select, update

from bot.db.engine import async_session_maker
from bot.db.models.users import User


async def get_user(tg_id: int):

    async with async_session_maker() as session:

        query = select(User).filter_by(tg_id=tg_id)
        result = await session.execute(query)
        return result.scalar_or_none()


async def create_user(user: User):

    async with async_session_maker() as session:

        await session.merge(user)
        await session.commit()


async def update_user(count_posts: int, tg_id):

    async with async_session_maker() as session:

        query = update(User).where(User.tg_id == tg_id).values(count_posts=count_posts)
        await session.execute(query)
        await session.commit()
