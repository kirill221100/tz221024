from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.utils.referral_code import get_referral_code
from schemes.registration import RegisterScheme
from db.utils.user import create_user, get_user_by_username_or_email
from security.password import hash_password


async def registration_func(reg_data: RegisterScheme, session: AsyncSession):
    if check_user := await get_user_by_username_or_email(reg_data.email, reg_data.username, session):
        if check_user.email == reg_data.email:
            raise HTTPException(status_code=409, detail='Пользователь с такой почтой уже существует')
        if check_user.username == reg_data.username:
            raise HTTPException(status_code=409, detail='Пользователь с таким именем уже существует')
    hashed_password = hash_password(reg_data.password.get_secret_value())
    if reg_data.referral_code:
        referral_code = await get_referral_code(reg_data.referral_code, session)
        if not referral_code:
            raise HTTPException(404, 'Реферальный код не найден')
        if not referral_code.is_active:
            raise HTTPException(400, 'Реферальный код неактивен')
        if referral_code.exp_date < datetime.utcnow():
            raise HTTPException(400, 'Срок годности реферального кода истёк')
        await create_user(reg_data.username, hashed_password, reg_data.email, session, referral_code)
    else:
        await create_user(reg_data.username, hashed_password, reg_data.email, session, None)
    return {'msg': 'Вы зарегистрировали аккаунт! Теперь аутентифицируйтесь.'}

