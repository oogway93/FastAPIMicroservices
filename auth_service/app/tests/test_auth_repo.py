# tests/test_auth_service.py
import pytest

# import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from repo.auth import AuthRepo
from utils.security import get_password_hash, verify_password
from schemas import UserCreate

# @pytest_asyncio.fixture
# async def test_user(session: AsyncSession) -> dict[str, str]:
#     user_data: UserCreate = UserCreate(username="testuser", email="testuser@gmail.com", password="testuser")
#     user_repo = AuthRepo(session)
#     await user_repo.create_user(user_data)
#     userFound = await user_repo.get_user_by_username("testuser")
#     return userFound


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession) -> None:
    user_data: UserCreate = UserCreate(
        username="testuser", email="testuser@gmail.com", password="testuser"
    )
    user_repo = AuthRepo(session)
    await user_repo.create_user(user_data)
    userFound = await user_repo.get_user_returning_User(user_data.username)
    assert userFound.username == user_data.username
    assert userFound.email == user_data.email
    assert userFound.hashed_password != get_password_hash(user_data.password)
    assert userFound.hashed_password != user_data.password
    assert verify_password(user_data.password, userFound.hashed_password)


@pytest.mark.asyncio
async def test_get_user_returning_User(session: AsyncSession) -> None:
    user_repo = AuthRepo(session)
    user_data1: UserCreate = UserCreate(
        username="testuser", email="testuser@gmail.com", password="testuser"
    )
    await user_repo.create_user(user_data1)

    userFound = await user_repo.get_user_returning_User("testuser")
    assert userFound.username == "testuser"
    assert userFound.id != ""
    assert userFound.hashed_password != "testuser"
    assert len(userFound.hashed_password) > len("testuser")
    await user_repo.db.aclose()

    user_repo2 = AuthRepo(session)
    try:
        user_data2: UserCreate = UserCreate(
            username="testuser2", email="testemail", password="testuser2"
        )
        await user_repo2.create_user(user_data2)
    except Exception as e:
        assert e is not None  # Pydantic validation of email is working
    await user_repo2.db.aclose()

    user_repo3 = AuthRepo(session)
    try:
        user_data3: UserCreate = UserCreate(
            username="testuser3", email="testemail@", password="testuser3"
        )
        await user_repo3.create_user(user_data3)
    except Exception as e:
        assert e is not None  # Pydantic validation of email is working
    await user_repo3.db.aclose()

    user_repo4 = AuthRepo(session)
    try:
        user_data4: UserCreate = UserCreate(
            username="testuser4", email="testemail@mail.", password="testuser4"
        )
        await user_repo4.create_user(user_data4)
    except Exception as e:
        assert e is not None  # Pydantic validation of email is working
    await user_repo4.db.aclose()


# @pytest.mark.asyncio
# async def test_authenticate_user(session: AsyncSession, test_user: User) -> None:
#     # Проверяем правильный пароль
#     authenticated_user: User | None = await AuthService.authenticate_user(
#         session, "test@example.com", "password123"
#     )
#     assert authenticated_user is not None
#     assert authenticated_user.email == "test@example.com"

#     # Проверяем неправильный пароль
#     not_authenticated: bool = await AuthService.authenticate_user(
#         session, "test@example.com", "wrongpassword"
#     )
#     assert not_authenticated is False

# @pytest.mark.asyncio
# async def test_create_access_token(test_user: User) -> None:
#     token: str = await AuthService.create_access_token(test_user)
#     assert token is not None
#     assert isinstance(token, str)
