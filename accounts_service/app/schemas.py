from pydantic import BaseModel, EmailStr
from uuid import UUID


class ProfileCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None


class Profile(ProfileCreate):
    user_id: UUID


class UserProfile(Profile):
    username: str
    email: EmailStr
