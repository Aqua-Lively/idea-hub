from sqlalchemy import select, case, func

from app.database import async_session_maker
from app.ideas.models import Idea
from app.ideas.schemas import SIdeaFull, SSortBy
from app.likes.models import Like
from app.repository.base import BaseRepository
from app.users.models import User


class IdeaRepository(BaseRepository):
    model = Idea
    @classmethod
    async def find_all(cls, user_id: int = -1, sort_by: SSortBy = SSortBy.date, desc: bool = True) -> list[SIdeaFull]:
        async with async_session_maker() as session:
            """
                SELECT
                    idea.id,
                    idea.content,
                    idea.is_anonim,
                    idea.is_posted,
                    idea.created_at,
                    CASE WHEN idea.is_anonim THEN NULL ELSE idea.user_id END as user_id,
                    CASE WHEN idea.is_anonim THEN NULL ELSE "user".first_name END as first_name,
                    CASE WHEN idea.is_anonim THEN NULL ELSE "user".last_name END as last_name,
                    COALESCE(BOOL_OR("like".user_id = user_id), FALSE) as like_for_user,
                    COUNT("like".idea_id) as count_likes
                FROM
                    idea
                LEFT JOIN
                    "like" ON idea.id = "like".idea_id
                LEFT JOIN
                    "user" ON idea.user_id = "user".id
                GROUP BY
                    idea.id, idea.content, idea.is_anonim, 
                    idea.is_posted, idea.created_at, idea.user_id, 
                    "user".first_name, "user".last_name
                ORDER BY
                    idea.created_at    <------ сортировка по дате либо по count_likes
            """
            query = select(
                cls.model.id,
                cls.model.content,
                cls.model.is_anonim,
                cls.model.is_posted,
                cls.model.created_at,
                case((cls.model.is_anonim, None), else_=cls.model.user_id).label('user_id'),
                case((cls.model.is_anonim, None), else_=User.first_name).label('first_name'),
                case((cls.model.is_anonim, None), else_=User.last_name).label('last_name'),
                func.coalesce(func.bool_or(Like.user_id == user_id), False).label('like_for_user'),
                func.count(Like.idea_id).label('count_likes')
            ).join(Like, cls.model.id == Like.idea_id, isouter=True).join(User, cls.model.user_id == User.id,
                                                                     isouter=True).group_by(
                cls.model.id,
                cls.model.content,
                cls.model.is_anonim,
                cls.model.is_posted,
                cls.model.created_at,
                cls.model.user_id,
                User.first_name,
                User.last_name
            )

            if sort_by == SSortBy.date:
                query = query.order_by(cls.model.created_at.desc() if desc else cls.model.created_at.asc())
            elif sort_by == SSortBy.like:
                query = query.order_by(func.count(Like.idea_id).desc() if desc else func.count(Like.idea_id).asc())

            result = await session.execute(query)

            idea_models = result.mappings().all()
            idea_schemas = [SIdeaFull.model_validate(idea_model) for idea_model in idea_models]

            return idea_schemas

    @classmethod
    async def find_all_my_ideas(
            cls,
            user_id: int,
            sort_by: SSortBy = SSortBy.date,
            desc: bool = True
    ) -> list[SIdeaFull]:
        async with async_session_maker() as session:
            """
                SELECT
                    idea.id,
                    idea.content,
                    idea.is_anonim,
                    idea.is_posted,
                    idea.created_at,
                    CASE WHEN idea.is_anonim THEN NULL ELSE idea.user_id END as user_id,
                    CASE WHEN idea.is_anonim THEN NULL ELSE "user".first_name END as first_name,
                    CASE WHEN idea.is_anonim THEN NULL ELSE "user".last_name END as last_name,
                    COALESCE(BOOL_OR("like".user_id = 1), FALSE) as like_for_user,
                    COUNT("like".idea_id) as count_likes
                FROM
                    idea
                LEFT JOIN
                    "like" ON idea.id = "like".idea_id
                LEFT JOIN
                    "user" ON idea.user_id = "user".id
                WHERE idea.user_id = 1
                GROUP BY
                    idea.id, idea.content, idea.is_anonim, 
                    idea.is_posted, idea.created_at, idea.user_id, 
                    "user".first_name, "user".last_name
                ORDER BY
                    idea.created_at 
            """

            query = select(
                cls.model.id,
                cls.model.content,
                cls.model.is_anonim,
                cls.model.is_posted,
                cls.model.created_at,
                case((cls.model.is_anonim, None), else_=cls.model.user_id).label('user_id'),
                case((cls.model.is_anonim, None), else_=User.first_name).label('first_name'),
                case((cls.model.is_anonim, None), else_=User.last_name).label('last_name'),
                func.coalesce(func.bool_or(Like.user_id == user_id), False).label('like_for_user'),
                func.count(Like.idea_id).label('count_likes')
            ).join(
                Like, cls.model.id == Like.idea_id, isouter=True
            ).join(
                User, cls.model.user_id == User.id, isouter=True
            ).filter(
                cls.model.user_id == user_id
            ).group_by(
                cls.model.id,
                cls.model.content,
                cls.model.is_anonim,
                cls.model.is_posted,
                cls.model.created_at,
                cls.model.user_id,
                User.first_name,
                User.last_name
            )

            if sort_by == SSortBy.date:
                query = query.order_by(cls.model.created_at.desc() if desc else cls.model.created_at.asc())
            elif sort_by == SSortBy.like:
                query = query.order_by(func.count(Like.idea_id).desc() if desc else func.count(Like.idea_id).asc())

            result = await session.execute(query)

            idea_models = result.mappings().all()
            idea_schemas = [SIdeaFull.model_validate(idea_model) for idea_model in idea_models]

            return idea_schemas
