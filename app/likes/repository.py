from select import select

from fastapi import HTTPException
from sqlalchemy import insert, delete

from app.database import async_session_maker
from app.ideas.repository import IdeaRepository
from app.likes.models import Like
from app.repository.base import BaseRepository


class LikeRepository(BaseRepository):
    model = Like

    @classmethod
    async def create_like(cls, idea_id: int, user_id: int) -> None:
        async with async_session_maker() as session:

            like_on_idea = await cls.find_one_or_none(idea_id=idea_id, user_id=user_id)

            if like_on_idea is not None:
                raise HTTPException(status_code=400, detail='Лайк пользователя уже есть у идеи')

            idea = await IdeaRepository.find_one_or_none(id=idea_id)
            if idea is None:
                raise HTTPException(status_code=400, detail='Не существует идеи')

            query = insert(cls.model).values(idea_id=idea_id, user_id=user_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_like(cls, idea_id: int, user_id: int) -> None:
        async with async_session_maker() as session:

            like_on_idea = await cls.find_one_or_none(idea_id=idea_id, user_id=user_id)

            if like_on_idea is None:
                raise HTTPException(status_code=400, detail='Лайк пользователя отсутствует у идеи')

            idea = await IdeaRepository.find_one_or_none(id=idea_id)
            if idea is None:
                raise HTTPException(status_code=400, detail='Не существует идеи')

            query = delete(cls.model).where(cls.model.id == like_on_idea.id)
            await session.execute(query)
            await session.commit()
