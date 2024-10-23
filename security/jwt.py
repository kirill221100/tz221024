from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException
from config import config


async def create_access_token(data: dict):
    exp = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = data.copy()
    token.update({'exp': exp})
    return jwt.encode(token, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM])
    except JWTError:
        raise HTTPException(401, detail='Invalid access token', headers={"WWW-Authenticate": "Bearer"})
