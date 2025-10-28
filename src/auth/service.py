#Purpose: Contains the database interaction logic for users. It takes validated data 
# (often from schemas), interacts with the database using the session and the User 
# model (models.py), and performs actions like finding, checking, or creating users.
# It's the "user department" in your back office.

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Optional

from src.books.models import User
from .schemas import UserCreate
from .utils import generate_pass_hash

class UserService():
    async def get_user_by_email(self,session: AsyncSession,email:str) -> Optional[User]:
        """Fetches a single user by email from the database."""
        statement= select(User).where(User.email== email)
        result= await session.exec(statement)
        return result.first()
    
    async def user_exists(self, session: AsyncSession, email:str) -> bool:
        """Checks if a user with the given email exists."""
        user= await self.get_user_by_email(session,email)
        return user is not None
    
    async def create_user(self,session:AsyncSession,email:str,user_data : UserCreate) ->User:
        """Creates a new user in the database."""
        # Check if user already exists (optional, could be done in route)
        # if await self.user_exists(session, user_data.email):
        #     raise ValueError("User with this email already exists") # Or custom exception

        # Hash the plain password securely
        hash_password=generate_pass_hash(user_data.password)
        
        # Create a dictionary of data for the User model
        # Exclude the plain password, include the hash
        user_db_data=user_data.model_dump(exclude={"password"})
        user_db_data["hash_password"]=hash_password
        
        # Create the database model instance
        new_user = User(**user_db_data)
        # Add to session (stage for saving)
        session.add(new_user)
        # Commit might be handled by the session dependency context manager
        # await session.commit()
        # Refresh to get DB-generated values like uid, created_at
        await session.refresh(new_user)

        return new_user