from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine, Base
from app.users.router import router as user_router
from app.ideas.router import router as idea_router
from app.likes.router import router as like_router

from app.users.models import User
from app.ideas.models import Idea
from app.likes.models import Like


@asynccontextmanager
async def lifespan(app: FastAPI):

    async def create_db_and_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_db_and_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    # print("Drop tables")
    # await drop_db_and_tables()
    print("Create tables")
    await create_db_and_tables()
    yield

app = FastAPI(
    title='idea-hab',
    lifespan=lifespan
)

app.include_router(user_router)
app.include_router(idea_router)
app.include_router(like_router)
