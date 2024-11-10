from datetime import datetime

from sqlalchemy import Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base
from app.ideas.models import Idea
from app.users.models import User


class Like(Base):
    __tablename__ = 'like'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    idea_id: Mapped[int] = mapped_column(ForeignKey('idea.id'))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
