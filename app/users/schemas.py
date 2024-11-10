from datetime import datetime

from pydantic import BaseModel, EmailStr


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUserAuthenticate(SUserLogin):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
