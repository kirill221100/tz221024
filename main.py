from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.db_setup import init_db
from redis_utils.redis_utils import redis
from config import config
from routes.auth import auth_router
import uvicorn

from routes.referral import referral_router
from routes.registration import registration_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await redis.create_connections()
    yield
    await redis.delete_connections()

app = FastAPI(lifespan=lifespan, debug=config.DEBUG, title='Тестовое')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(registration_router, prefix='/registration', tags=['registration'])
app.include_router(referral_router, prefix='/referral', tags=['referral'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, timeout_keep_alive=60, port=8000)
