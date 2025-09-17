from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from schemas import Profile, ProfileCreate, UserProfile
from dependencies import get_current_user
from repo.profile import ProfileRepo
from database import get_session

router = APIRouter()


@router.put("/profile", status_code=status.HTTP_201_CREATED)
async def update_profile(
    user_profile_data: ProfileCreate,
    current_user: dict[str, str] = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    repo = ProfileRepo(db)
    updated_profile = await repo.update_user_profile(
        current_user["id"], user_profile_data
    )
    return updated_profile


@router.post("/profile", status_code=status.HTTP_201_CREATED)
async def create_profile(
    user_profile_data: Profile,
    db: AsyncSession = Depends(get_session),
):
    repo = ProfileRepo(db)
    profile_id = await repo.create_user_profile(user_profile_data)
    return {"profile_id": profile_id}


@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_profile(
    current_user: dict[str, str] = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    profile_repo = ProfileRepo(db)
    foundData = await profile_repo.get_user_profile_by_user_id(current_user["id"])
    curr_user_profile = UserProfile(
        user_id=foundData.user_id,
        first_name=foundData.first_name,
        last_name=foundData.last_name,
        address=foundData.address,
        username=current_user["username"],
        email=current_user["email"],
    )
    return curr_user_profile
