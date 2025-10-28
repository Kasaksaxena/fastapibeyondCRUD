from pydantic import BaseModel, EmailStr,Field 
from typing import Optional
import uuid 
from datetime import datetime

# Schema for data needed during SIGN UP (Request Body)
class UserCreate(BaseModel):
    username: str =Field(min_length=3, max_length=8)
    email : EmailStr
    password: str=Field(min_length= 8)
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    
# Schema for data returned AFTER successful creation or when fetching user info (Response Body)
class UserRead(BaseModel):
        uid:uuid.UUID
        username:str
        email : EmailStr
        first_name: Optional[str] = None
        last_name: Optional[str] = None
        is_verified: bool
        created_at: datetime
    # NO password_hash here for security!
    # Pydantic config to allow creating from ORM model instances
        class Config:
          from_attributes = True
    
# Schema for data needed during LOGIN (Request Body)
class UserLogin(BaseModel):
    email: EmailStr # Or username, depending on your login logic
    password: str # Takes the PLAIN password input