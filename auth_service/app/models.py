from sqlmodel import Field, SQLModel
from uuid import UUID
import uuid


class User(SQLModel, table=True):

    __tablename__ = "users"  # type: ignore

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True, index=True)
    hashed_password: str = Field(nullable=False)
