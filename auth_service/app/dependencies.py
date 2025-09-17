from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from repo.auth import AuthRepo
from utils.security import decode_token
from database import get_session

security = HTTPBearer(
    description="Put your JWT token here and entertain with handlers "
)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: AsyncSession = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(credentials.credentials)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user_repo = AuthRepo(db)
    user = await user_repo.get_user_returning_User(username)
    if user is None:
        raise credentials_exception

    return user
