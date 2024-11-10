from fastapi import APIRouter, Depends

from app.likes.repository import LikeRepository
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix='/likes',
    tags=['Лайки']
)


@router.post('')
async def put_like(idea_id: int, current_user: User = Depends(get_current_user)):
    await LikeRepository.create_like(idea_id=idea_id, user_id=current_user.id)


@router.delete('')
async def remove_like(idea_id: int, current_user: User = Depends(get_current_user)):
    await LikeRepository.delete_like(idea_id=idea_id, user_id=current_user.id)