from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_HOST: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFERRAL_EXPIRE_TIME_MINUTES: int
    JWT_SECRET_KEY: str
    ALGORITHM: str
    DEBUG: bool
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_config():
    return Config()
