# src/books/routes.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
import uuid

# Import schemas
from .schema import BookRead, BookCreate, BookUpdate
# Import the service
from .service import BookService
# Import session dependency and session type
from src.db.connection import get_session, AsyncSession
# Import dependency for getting current user (assuming it exists)
# from src.auth.dependencies import get_current_user
# from src.db.models import User # If needed for current user type hint

# Create the router instance
book_router = APIRouter()

# --- CRUD Endpoints Defined on the Router ---

@book_router.get("/", response_model=List[BookRead])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    service: BookService = Depends(BookService) # Inject service
):
    """Retrieves a list of all books."""
    books = await service.get_all_books(session)
    return books

@book_router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    session: AsyncSession = Depends(get_session),
    service: BookService = Depends(BookService),
    # Get current user to associate book with them
    # current_user: User = Depends(get_current_user) # Uncomment if auth is set up
):
    """Creates a new book."""
    # Replace with actual user ID from logged-in user
    # For now, using a placeholder - REQUIRES AUTHENTICATION SETUP
    placeholder_user_id = uuid.uuid4() # *** REPLACE THIS ***
    new_book = await service.create_book(session, book_data, placeholder_user_id) # Pass user ID
    return new_book

@book_router.get("/{book_uid}", response_model=BookRead)
async def get_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    service: BookService = Depends(BookService)
):
    """Retrieves a single book by its UID."""
    book = await service.get_book_by_uid(session, book_uid)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with UID {book_uid} not found"
        )
    return book

@book_router.patch("/{book_uid}", response_model=BookRead)
async def update_book(
    book_uid: uuid.UUID,
    book_update_data: BookUpdate,
    session: AsyncSession = Depends(get_session),
    service: BookService = Depends(BookService)
    # Add check: current_user: User = Depends(get_current_user)
    # Add logic: Check if current_user owns the book before updating
):
    """Updates fields of an existing book."""
    updated_book = await service.update_book(session, book_uid, book_update_data)
    if updated_book is None:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with UID {book_uid} not found"
        )
    # Add authorization check here in a real app
    return updated_book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    service: BookService = Depends(BookService)
    # Add check: current_user: User = Depends(get_current_user)
    # Add logic: Check if current_user owns the book before deleting
):
    """Deletes a book by its UID."""
    deleted = await service.delete_book(session, book_uid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with UID {book_uid} not found"
        )
    # Add authorization check here in a real app
    return None # Return None for 204 status