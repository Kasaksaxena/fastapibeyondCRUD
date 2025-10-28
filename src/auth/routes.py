#Purpose: This is the actual web endpoint (like /api/v1/auth/signup) that 
# the outside world (a website, a mobile app) interacts with to create a 
# new user account. It acts as the public-facing entry point for registration.

from fastapi import APIRouter,Depends,HTTPException,status
import uuid
from .schemas import UserCreate,UserRead
from .service import UserService
from src.db.connection import get_session,AsyncSession

auth_router=APIRouter()

@auth_router.post("/signup",
                  response_model=UserRead,# Tells FastAPI the response should look like UserRead
                  status_code=status.HTTP_201_CREATED)
async  def signup_user(user_data: UserCreate,# FastAPI gets this from the JSON request body
                       session:AsyncSession = Depends(get_session),
                       service: UserService = Depends(UserService) # Gets UserService instance via dependency
                       ):
    """Handles new user registration."""
    # 1. Check if user already exists
    user_exists = await service.user_exists(session=session, email=user_data.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, # Or 409 Conflict
            detail="Email already registered."
        )

    # 2. If not exists, create the user via the service
    new_user = await service.create_user(session=session, user_data=user_data)

    # 3. Return the newly created user data (serialized by UserRead)
    return new_user