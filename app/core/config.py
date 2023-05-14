# app/core/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "База ситуаций для переговорных поединков"
    description: str = "База ситуаций для переговорных поединков"
    database_url: str = "sqlite+aiosqlite:///./duellio.db"

    class Config:
        env_file = ".env"


settings = Settings()
