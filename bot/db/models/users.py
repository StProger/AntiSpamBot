from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger

from bot.db.engine import Base


class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str]
    name: Mapped[str]
    count_posts: Mapped[int] = mapped_column(default=0)
