from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from typing import List
import datetime


class ReferralCode(Base):
    __tablename__ = 'referral_codes'
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    referrer: Mapped["User"] = relationship(back_populates='ref_codes', foreign_keys=[referrer_id])
    exp_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    referrals: Mapped[List["User"]] = relationship(back_populates='register_ref_code', foreign_keys="User.register_ref_code_id")