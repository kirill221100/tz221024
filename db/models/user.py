from db.db_setup import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    ref_codes: Mapped[List["ReferralCode"]] = relationship(back_populates='referrer', foreign_keys="ReferralCode.referrer_id")
    register_ref_code_id: Mapped[int] = mapped_column(ForeignKey('referral_codes.id'), nullable=True)
    register_ref_code: Mapped["ReferralCode"] = relationship(back_populates='referrals',
                                                                  foreign_keys=[register_ref_code_id])
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
