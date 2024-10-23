from typing import Optional
from pydantic import BaseModel, EmailStr, Field, SecretStr


class RegisterScheme(BaseModel):
    username: str = Field(min_length=2, max_length=32)
    password: SecretStr  = Field(min_length=6, max_length=32)
    email: EmailStr
    referral_code: Optional[str] = None

class RegistrationResponse(BaseModel):
    msg: str
