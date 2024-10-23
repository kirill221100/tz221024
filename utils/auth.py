from fastapi import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.utils.user import get_user_by_username
from security.password import verify_pass
from security.jwt import create_access_token


async def auth_func(auth_data: OAuth2PasswordRequestForm, session: AsyncSession):
    user = await get_user_by_username(auth_data.username, session)
    if verify_pass(auth_data.password, user.hashed_password):
        data = {'id': user.id}
        access_token = await create_access_token(data)
        return {'access_token': access_token, 'token_type': 'bearer'}
    raise HTTPException(401, 'Неправильное имя или пароль')
