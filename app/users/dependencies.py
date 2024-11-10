from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import UserIsNotPresentException, TokenExpiredException, IncorrectTokenFormatException, \
    TokenAbsentException
from app.users.repository import UserRepository


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token


def get_token_or_none(request: Request):
    token = request.cookies.get('booking_access_token')
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    user = await UserRepository.find_by_id(int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user


async def get_current_user_or_none(token: str | None = Depends(get_token_or_none)):
    if token is None:
        return None
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    user = await UserRepository.find_by_id(int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user
