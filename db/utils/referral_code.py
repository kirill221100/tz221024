import datetime
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from db.models.referral_code import ReferralCode
from db.models.user import User

async def create_referral_code(exp_date_utc: datetime.datetime, code: str, referrer: User, session: AsyncSession):
    referral_code = ReferralCode(code=code, referrer=referrer, exp_date=exp_date_utc)
    session.add(referral_code)
    await session.commit()

async def get_referral_code(code: str, session: AsyncSession):
    return (await session.execute(select(ReferralCode).filter_by(code=code))).scalar_one_or_none()


async def get_active_referral_code(referrer_id: int, session: AsyncSession):
    return (await session.execute(select(ReferralCode).filter_by(referrer_id=referrer_id, is_active=True))).scalar_one_or_none()


async def get_referral_code_by_email(email: EmailStr, session: AsyncSession):
    return (
        await session.execute(
            select(ReferralCode).filter_by(is_active=True).join(User, User.email == email)
        )
    ).scalar_one_or_none()

async def get_referral_codes_user_selectin(referrer_id: int, session: AsyncSession):
    return (await session.execute(select(ReferralCode).filter_by(referrer_id=referrer_id).options(selectinload(ReferralCode.referrals)))).scalars().all()
