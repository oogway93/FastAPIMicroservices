from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

async_engine = create_async_engine(
    url="postgresql+asyncpg://postgres:postgres@auth_db:5432/auth_db", echo=True
)


async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Инициализация базы данных (создание таблиц)"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def shutdown_db():
    """Инициализация базы данных (создание таблиц)"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
