# src/books/service.py
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid
from typing import List, Optional

# Import the Database model and Pydantic schemas
from src.books.models import Book, User 
from .schema import BookCreate, BookUpdate

class BookService:
    async def get_all_books(self, session: AsyncSession) -> List[Book]:
        statement = select(Book).order_by(Book.created_at.desc())
        result = await session.exec(statement)
        return result.all()

    async def get_book_by_uid(self, session: AsyncSession, book_uid: uuid.UUID) -> Optional[Book]:
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        return result.first()

    async def create_book(self, session: AsyncSession, book_data: BookCreate, user_uid: uuid.UUID) -> Book:
        # Create dictionary from schema, add owner
        book_dict = book_data.model_dump()
        book_dict["user_uid"] = user_uid # Set the owner

        # Create the database model instance
        new_book = Book(**book_dict)

        session.add(new_book)
        # Commit handled by get_session dependency context manager usually
        # await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(
        self, session: AsyncSession, book_uid: uuid.UUID, update_data: BookUpdate
    ) -> Optional[Book]:
        book_to_update = await self.get_book_by_uid(session, book_uid)
        if not book_to_update:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(book_to_update, key, value)

        session.add(book_to_update)
        # await session.commit()
        await session.refresh(book_to_update)
        return book_to_update

    async def delete_book(self, session: AsyncSession, book_uid: uuid.UUID) -> bool:
        book_to_delete = await self.get_book_by_uid(session, book_uid)
        if not book_to_delete:
            return False # Indicate not found

        await session.delete(book_to_delete)
        # await session.commit()
        return True # Indicate success