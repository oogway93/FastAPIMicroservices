from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine


from main import app
from database import get_session, SQLModel

# Тестовая БД (SQLite в памяти)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def engine() -> AsyncGenerator[AsyncEngine, Any]:
    # Создаем тестовый движок
    engine: AsyncEngine = create_async_engine(
        TEST_DATABASE_URL, echo=False, future=True
    )

    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Удаляем таблицы после завершения
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, Any]:
    # Создаем тестовую сессию
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, Any]:
    # Переопределяем зависимость get_session для тестов
    async def override_get_session() -> AsyncGenerator[AsyncSession, Any]:
        yield session

    app.dependency_overrides[get_session] = override_get_session

    # Создаем тестового клиента
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client

    app.dependency_overrides.clear()
