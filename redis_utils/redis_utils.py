import json
from datetime import datetime
from redis import asyncio as aioredis
from config import config


class Redis:
    def __init__(self):
        self.url = f"redis://:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}"
        self.connection = None

    async def create_connections(self) -> None:
        self.connection = aioredis.from_url(self.url, db=0)

    async def delete_connections(self) -> None:
        await self.connection.aclose()


redis = Redis()


async def set_referral_code(email: str, code: str, exp_date: datetime):
    data = {"code": code, "exp_date": str(exp_date)}
    await redis.connection.set(email, json.dumps(data), ex=1800)


async def get_referral_code_by_email(email: str):
    if code := await redis.connection.get(email):
        code_json = json.loads(str(code, encoding='utf-8'))
        return code_json
    return False


async def delete_referral_code_by_email(email: str):
    await redis.connection.delete(email)

