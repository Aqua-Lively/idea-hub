from datetime import date, datetime

from sqlalchemy import Integer, String, Boolean, TIMESTAMP, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Idea(Base):
    __tablename__ = 'idea'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    is_anonim: Mapped[bool] = mapped_column(Boolean)
    is_posted: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
