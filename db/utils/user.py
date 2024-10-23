from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.referral_code import ReferralCode
from db.models.user import User
from pydantic import EmailStr
from typing import Optional


async def get_user_by_username(username: str, session: AsyncSession):
    return (await session.execute(select(User).filter_by(username=username))).scalar_one_or_none()


async def get_user_by_email(email: EmailStr, session: AsyncSession):
    return (await session.execute(select(User).filter_by(email=email))).scalar_one_or_none()


async def get_user_by_id(user_id: int, session: AsyncSession):
    return (await session.execute(select(User).filter_by(id=user_id))).scalar_one_or_none()


async def get_user_by_username_or_email(email: EmailStr, username: str, session: AsyncSession):
    return (await session.execute(select(User).filter(or_(User.username == username, User.email == email)))).scalar_one_or_none()

async def create_user(username: str, hashed_password: str, email: EmailStr, session: AsyncSession,
                      referral_code: Optional[ReferralCode] = None):
    if referral_code:
        user = User(username=username, hashed_password=hashed_password, email=email, register_ref_code=referral_code)
    else:
        user = User(username=username, hashed_password=hashed_password, email=email)
    session.add(user)
    await session.commit()
    return user



