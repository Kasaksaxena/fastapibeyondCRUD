from pydantic import BaseModel
from typing import Optional
class Book(BaseModel):
    id:int
    title:str
    author:str
    publisher:Optional[str]
    publish_date:Optional[str]
    page_count:Optional[int]
    language:Optional[str]
    
class BookCreateModel(BaseModel):
    id:int
    title:str
    author:str
    publisher:Optional[str]
    publish_date:Optional[str]
    page_count:Optional[int]
    language:Optional[str]
  
class BookUpdateModel(BaseModel):
    
    title:Optional[str]
    author:Optional[str]
    publisher:Optional[str]
    page_count: Optional[int] = None
    language: Optional[str] = None
    