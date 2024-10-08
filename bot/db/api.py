from sqlalchemy import select, update, Result
from aiogram import types
from asyncio import sleep

from bot.db.engine import async_session_maker
from bot.db.models.users import User


async def get_user(tg_id: int):

    async with async_session_maker() as session:

        query = select(User).filter_by(tg_id=tg_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def create_user(user: User):

    async with async_session_maker() as session:

        await session.merge(user)
        await session.commit()


async def update_user(count_posts: int, tg_id):

    async with async_session_maker() as session:

        query = update(User).where(User.tg_id == tg_id).values(count_posts=count_posts)
        await session.execute(query)
        await session.commit()

async def update_count_warnings(tg_id, count_warnings):
    async with async_session_maker() as session:
        query = update(User).where(User.tg_id == tg_id).values(warning_count=count_warnings)
        await session.execute(query)
        await session.commit()

async def update_last_message_id_work(tg_id, message_id):
    async with async_session_maker() as session:
        query = update(User).where(User.tg_id == tg_id).values(last_message_id_work=message_id)
        await session.execute(query)
        await session.commit()

async def update_last_message_id_las_vegas(tg_id, message_id):
    async with async_session_maker() as session:
        query = update(User).where(User.tg_id == tg_id).values(last_message_id_las_vegas=message_id)
        await session.execute(query)
        await session.commit()


async def update_count_posts():

    async with async_session_maker() as session:

        query = update(User).values(count_posts=0, warning_count=0)
        await session.execute(query)
        await session.commit()


async def delete_mes(message: types.Message):

    await sleep(10)
    await message.delete()


async def find_tg_id(username: str):

    async with async_session_maker() as session:

        stmt = (
            select(User)
            .where(User.username == username)
        )

        result: Result = await session.execute(stmt)

        return result.scalar_one_or_none()