from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from pydantic import EmailStr
from typing import List
from schemes.referral import GetReferrals, CreateOrGetCodeResponse, DeleteCodeResponse
from security.auth import get_current_user
from utils.referral import (create_referral_code_func, get_code_by_email_func, get_referrals_func,
                            delete_referral_code_func)

referral_router = APIRouter()

@referral_router.post('/create-code', response_model=CreateOrGetCodeResponse)
async def create_code_path(user=Depends(get_current_user),
                           session: AsyncSession = Depends(get_session)):
    """Создать реферальный код"""
    return await create_referral_code_func(user['id'], session)


@referral_router.delete('/delete-code', response_model=DeleteCodeResponse)
async def delete_code_path(code: str, user=Depends(get_current_user),
                           session: AsyncSession = Depends(get_session)):
    """Удалить реферальный код"""
    return await delete_referral_code_func(code, user['id'], session)


@referral_router.get('/get-code', response_model=CreateOrGetCodeResponse)
async def get_code_path(referer_email: EmailStr, session: AsyncSession = Depends(get_session)):
    """Получить реферальный код по email реферера"""
    return await get_code_by_email_func(referer_email, session)


@referral_router.get('/get-referrals', response_model=List[GetReferrals])
async def get_referrals_path(referrer_id: int, session: AsyncSession = Depends(get_session)):
    """Получить информацию о рефералах по id реферера"""
    return await get_referrals_func(referrer_id, session)
