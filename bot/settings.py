from pydantic_settings import BaseSettings, SettingsConfigDict

import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):

    BOT_TOKEN: str = os.getenv('BOT_TOKEN')

    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")

    # Путь к логам
    PATH_LOGS: str = "bot/data/logs.log"

    model_config = SettingsConfigDict(env_file="../.env")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
BOT_SCHEDULER = AsyncIOScheduler(timezone="Europe/Moscow")