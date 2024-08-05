from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from bot.settings import settings


DATABASE_URL = settings.db_url
DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):

    def as_dict(self) -> dict:

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


async def get_session() -> AsyncSession:

    async with async_session_maker() as session:
        yield session
