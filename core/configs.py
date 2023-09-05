from typing import List
from pydantic import BaseConfig
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseConfig):
    API_VERSION = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://fastapi:fastapi@localhost:15432/fastapi'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()