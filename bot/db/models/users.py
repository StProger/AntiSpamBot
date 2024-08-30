from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer

from bot.db.engine import Base



class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str]
    name: Mapped[str]
    count_posts: Mapped[int] = mapped_column(default=0)
    warning_count: Mapped[int] = mapped_column(default=0)
    last_message_id_work: Mapped[int] = mapped_column(BigInteger, default=None)
    last_message_id_las_vegas: Mapped[int] = mapped_column(BigInteger, default=None)
