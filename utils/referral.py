import secrets
import datetime
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from redis_utils.redis_utils import set_referral_code, get_referral_code_by_email, delete_referral_code_by_email
from db.utils.referral_code import create_referral_code, get_referral_codes_user_selectin, \
    get_referral_code_by_email as get_referral_code_by_email_db, get_active_referral_code, get_referral_code
from db.utils.user import get_user_by_id, get_user_by_email
from config import config

async def create_referral_code_func(user_id: int, session: AsyncSession):
    referrer = await get_user_by_id(user_id, session)
    active_code = await get_active_referral_code(user_id, session)
    if active_code:
        active_code.is_active = False
    code = secrets.token_urlsafe(20)
    exp_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=config.REFERRAL_EXPIRE_TIME_MINUTES)
    await create_referral_code(exp_date, code, referrer, session)
    if await get_referral_code_by_email(referrer.email):
        await set_referral_code(referrer.email, code, exp_date)
    return {'code': code}

async def delete_referral_code_func(code: str, user_id: int, session: AsyncSession):
    code_db = await get_referral_code(code, session)
    if code_db:
        referrer = await get_user_by_id(user_id, session)
        if referrer.id == code_db.referrer_id:
            await session.delete(code_db)
            await session.commit()
            await delete_referral_code_by_email(referrer.email)
            return {'msg': 'Реферальный код удалён'}
        raise HTTPException(403, 'Вы не реферер этого кода')
    raise HTTPException(404, 'Реферальный код не найден')

async def get_code_by_email_func(email: EmailStr, session: AsyncSession):
    if await get_user_by_email(email, session):
        code = await get_referral_code_by_email(email)
        if not code:
            code_db = await get_referral_code_by_email_db(email, session)
            if code_db:
                await set_referral_code(email, code_db.code, code_db.exp_date)
                return {'code': code_db.code}
            raise HTTPException(404, 'Нет подходящего реферального кода')
        return {'code': code['code']}
    raise HTTPException(404, 'Нет реферера с таким email')


async def get_referrals_func(referer_id: int, session: AsyncSession):
    if await get_user_by_id(referer_id, session):
        referral_codes = await get_referral_codes_user_selectin(referer_id, session)
        result = []
        for i in referral_codes:
            for j in i.referrals:
                j.__dict__['register_ref_code'] = i.code
                result.append(j)
        return result
    raise HTTPException(404, 'Нет реферера с таким id')

