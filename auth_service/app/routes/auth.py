from datetime import timedelta
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from redisService import AsyncRedis
from dependencies import get_current_user
from models import User
from utils.security import create_access_token
from database import get_session
from schemas import Token, UserCreate, UserLogin
from repo.auth import AuthRepo


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(req_data: UserCreate, db: AsyncSession = Depends(get_session)):
    user_repo = AuthRepo(db)
    await user_repo.create_user(req_data)
    result = await user_repo.get_user_by_username_returning_ids(req_data.username)
    return result


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(req_data: UserLogin, db: AsyncSession = Depends(get_session)):
    user_repo = AuthRepo(db)
    check = await user_repo.verifing_user(req_data)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    ids = await user_repo.get_user_by_username_returning_ids(req_data.username)
    if not ids:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": req_data.username, "user_id": ids["user_id"]},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users_credentials(current_user: User = Depends(get_current_user)):
    redis = await AsyncRedis().connect()
    found = await redis.get(current_user.username)
    if found is not None:
        return {"current user info": json.loads(found)}
    isAdd = await redis.set(current_user.username, current_user.model_dump_json(), expire=60)
    if not isAdd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Nil information about users credentials")
    return {"current user info": current_user }
    
    
