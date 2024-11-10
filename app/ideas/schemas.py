from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class SIdeaAdd(BaseModel):
    content: str
    is_anonim: bool


class SIdea(BaseModel):
    id: int
    content: str
    is_anonim: bool
    is_posted: bool
    created_at: datetime
    user_id: int | None


class SIdeaFull(BaseModel):
    id: int
    content: str
    is_anonim: bool
    is_posted: bool
    created_at: datetime
    user_id: int | None
    first_name: str | None
    last_name: str | None
    like_for_user: bool
    count_likes: int


class SSortBy(Enum):
    date = 'data'
    like = 'like'
