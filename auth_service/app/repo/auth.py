import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from service.auth import AuthService
from utils.security import get_password_hash, verify_password
from schemas import UserCreate, UserLogin
from models import User


class AuthRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate):
        tranc = await self.db.begin()
        new_auth_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
        )
        self.db.add(new_auth_user)
        await tranc.commit()
        await self.db.close()

    async def get_user_by_username_returning_ids(self, username: str):
        try:
            stmt = await self.db.exec(select(User).where(User.username == username))
            found = stmt.one()

            auth_service = AuthService()
            result = await auth_service.create_account(found.id)

            return {"user_id": str(found.id), "profile_id": result}
        except Exception as e:
            raise e

    async def get_user_returning_User(self, username: str) -> User:
        try:
            stmt = await self.db.exec(select(User).where(User.username == username))
            found = stmt.one()
            return found
        except Exception as e:
            print(f"Error in getting user: {e}")
            return User(
                id=uuid.UUID(int=0),
                email="notfound@gmail.com",
                username="notfound",
                hashed_password="notfound",
            )

    async def verifing_user(self, login_data: UserLogin):
        try:
            stmt = await self.db.exec(
                select(User).where(User.username == login_data.username)
            )
            found = stmt.one_or_none()
            if found is None:
                print(f"Error: not finding an user: {login_data.username}")
                return None
            check_password = verify_password(login_data.password, found.hashed_password)
            if not check_password:
                print(f"Error: matching password from login form and from db")
                return None
            return found
        except Exception as e:
            print(f"Error in varifing user: {e}")
            return None
