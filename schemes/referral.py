from pydantic import BaseModel, EmailStr


class GetReferrals(BaseModel):
    id: int
    username: str
    email: EmailStr
    register_ref_code: str


class CreateOrGetCodeResponse(BaseModel):
    code: str


class DeleteCodeResponse(BaseModel):
    msg: str
