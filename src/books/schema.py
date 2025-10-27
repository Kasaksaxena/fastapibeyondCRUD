# src/books/schemas.py
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import date # Use date if model uses date

# Schema for returning book data (might exclude sensitive fields if any)
class BookRead(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: Optional[str] = None
    publish_date: Optional[date] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
    user_uid: Optional[uuid.UUID] = None # Include owner ID if needed

# Schema for creating a book (data client sends)
class BookCreate(BaseModel):
    title: str
    author: str
    publisher: Optional[str] = None
    publish_date: Optional[date] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
    # user_uid is usually set based on logged-in user, not sent by client

# Schema for updating a book (all fields optional)
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publish_date: Optional[date] = None
    page_count: Optional[int] = None
    language: Optional[str] = None