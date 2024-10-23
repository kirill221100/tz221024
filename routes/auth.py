from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from schemes.auth import AuthResponseScheme
from utils.auth import auth_func

auth_router = APIRouter()

@auth_router.post('/', response_model=AuthResponseScheme)
async def auth_path(auth_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    """Аутентификация"""
    return await auth_func(auth_data, session)

