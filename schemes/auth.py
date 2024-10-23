from pydantic import BaseModel


class AuthResponseScheme(BaseModel):
    access_token: str
    token_type: str
