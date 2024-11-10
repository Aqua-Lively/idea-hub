from fastapi import APIRouter, Depends

from app.ideas.repository import IdeaRepository
from app.ideas.schemas import SIdeaAdd, SSortBy, SIdeaFull
from app.users.dependencies import get_current_user, get_current_user_or_none
from app.users.models import User

router = APIRouter(
    prefix='/ideas',
    tags=['Идеи']
)


@router.get('')
async def get_ideas(
        sort_by: SSortBy = SSortBy.date,
        desc: bool = True,
        current_user: User | None = Depends(get_current_user_or_none)
) -> list[SIdeaFull]:
    if current_user:
        ideas = await IdeaRepository.find_all(user_id=current_user.id, sort_by=sort_by, desc=desc)
    else:
        ideas = await IdeaRepository.find_all(sort_by=sort_by, desc=desc)
    return ideas


@router.post('')
async def create_idea(idea: SIdeaAdd, current_user: User = Depends(get_current_user)) -> None:
    idea_dict = idea.model_dump()
    idea_dict['user_id'] = current_user.id
    idea_dict['is_posted'] = False

    await IdeaRepository.add(**idea_dict)


@router.get('/my')
async def get_my_ideas(
        sort_by: SSortBy = SSortBy.date,
        desc: bool = True,
        current_user: User = Depends(get_current_user)
) -> list[SIdeaFull]:
    current_user_ideas = await IdeaRepository.find_all_my_ideas(user_id=current_user.id, sort_by=sort_by, desc=desc)

    return current_user_ideas
