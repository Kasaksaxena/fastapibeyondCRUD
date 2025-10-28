from sqlmodel import SQLModel,Field,Relationship
import uuid
from typing import Optional,List
from datetime import datetime,date

# --- User Model Example (if needed for relationships) ---
class User(SQLModel, table=True):
     __tablename__ = "users" # Example table name
     uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
     email: str = Field(unique=True, index=True ,max_length=100,nullable=False)
     password_hash:str = Field(nullable=False) # Store the SECURE HASH, not the password
     first_name: Optional[str] = Field(default=None, max_length=50)
     last_name: Optional[str] = Field(default=None, max_length=50)
     is_verified : bool =Field(default=False,nullable=False)
     created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
     updated_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"onupdate": datetime.utcnow} # Auto-updates on modification
    )
     
     # Define relationship back to books (one user -> many books)
     books: List["Book"] = Relationship(back_populates="user")
  
class Review(SQLModel,table=True):
     pass   
class Book(SQLModel,table=True):
    __tablename__="books"
    uid: uuid.UUID=Field(default_factory=uuid.uuid4, primary_key=True,nullable=True)
    title: str
    author: str
    page_count: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    # Foreign Key to link Book back to User
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid", nullable=True) # Matches User.uid
    # Define relationship to User (many books -> one user)
    user: Optional[User] = Relationship(back_populates="books")
    # Defines the one-to-many relationship: One User can write many Reviews
    reviews: List["Review"]=Relationship(back_populates="user")