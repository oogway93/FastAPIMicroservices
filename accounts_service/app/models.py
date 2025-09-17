from decimal import Decimal
from uuid import UUID
import uuid
from sqlmodel import Field, SQLModel


class BankAccount(SQLModel, table=True):
    __tablename__ = "bank_accounts"  # type: ignore

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(index=True)  # reference to user in Auth Service
    account_number: str = Field(unique=True, index=True)
    balance: Decimal = Field(default=0, max_digits=12, decimal_places=2)
    currency: str = Field(default="USD")


class Profile(SQLModel, table=True):
    __tablename__ = "user_profiles"  # type: ignore

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(unique=True, index=True)
    first_name: str | None = Field(nullable=True)
    last_name: str | None = Field(nullable=True)
    address: str | None = Field(nullable=True)
