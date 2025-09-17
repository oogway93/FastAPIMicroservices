from uuid import UUID
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from schemas import Profile as ProfileSchema
from schemas import ProfileCreate
from models import Profile


class ProfileRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user_profile(self, user_profile_data: ProfileSchema) -> UUID:
        tranc = await self.db.begin()
        new_user_profile = Profile(
            user_id=user_profile_data.user_id,
            first_name=user_profile_data.first_name,
            last_name=user_profile_data.last_name,
            address=user_profile_data.address,
        )
        self.db.add(new_user_profile)
        await tranc.commit()
        await self.db.refresh(new_user_profile)

        stmt = await self.db.exec(
            select(Profile).where(Profile.user_id == user_profile_data.user_id)
        )
        found = stmt.one()
        if len(str(found.id)) == 0:
            return uuid.UUID(int=0)

        return found.id

    async def update_user_profile(
        self, user_id: str, user_profile_data: ProfileCreate
    ) -> Profile:
        tranc = await self.db.begin()
        userFound = await self.get_user_profile_by_user_id(user_id)
        for key, value in user_profile_data.model_dump().items():
            if value != "string":
                if hasattr(userFound, key):
                    setattr(userFound, key, value)
        await tranc.commit()
        return userFound

    async def get_user_profile_by_user_id(self, user_id: str) -> Profile:
        try:
            stmt = await self.db.exec(select(Profile).where(Profile.user_id == user_id))
            found = stmt.one()
            return found
        except Exception as e:
            print(f"Error in getting user: {e}")
            return Profile(
                id=uuid.UUID(int=0),
                user_id=uuid.UUID(int=0),
                first_name="",
                last_name="",
                address="",
            )
