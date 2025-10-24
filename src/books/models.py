from sqlmodel import SQLModel,Field
import uuid
from typing import Optional
from datetime import datetime

class Book(SQLModel,table=True):
    __tablename__="books"
    uid: uuid.UUID=Field(default_factory=uuid.uuid4, primary_key=True,nullable=True)
    title: str
    author: str
    page_count: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    