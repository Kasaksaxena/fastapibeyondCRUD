# src/books/routes.py
from fastapi import APIRouter, HTTPException, status
from typing import List

# Import schemas from the schemas.py file in the same directory
from .schema import Book, BookCreateModel, BookUpdateModel

# Create the router instance specifically for books
book_router = APIRouter()

# --- In-Memory "Database" (Should ideally be moved elsewhere in a real app) ---
BOOKS = [
    {
        "id": 1,
        "title": "Head First Python",
        "author": "Paul Barry",
        "publisher": "O'Reilly Media",
        "publish_date": "2016-12-19",
        "page_count": 626,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Learning Python",
        "author": "Mark Lutz",
        "publisher": "O'Reilly Media",
        "publish_date": "2013-06-14",
        "page_count": 1648,
        "language": "English",
    },
     {
        "id": 3,
        "title": "Automate the Boring Stuff with Python",
        "author": "Al Sweigart",
        "publisher": "No Starch Press",
        "publish_date": "2019-11-12",
        "page_count": 592,
        "language": "English",
    },
]

# Helper function to find a book by ID
def find_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None

# --- CRUD Endpoints Defined on the Router ---

# READ ALL Books (Path is "/" relative to router prefix)
@book_router.get("/", response_model=List[Book])
async def get_all_books():
    """Retrieves a list of all books."""
    return BOOKS

# CREATE Book (Path is "/" relative to router prefix)
@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel):
    """Creates a new book."""
    new_book_dict = book_data.model_dump()
    BOOKS.append(new_book_dict)
    return new_book_dict

# READ SINGLE Book (Path includes parameter relative to prefix)
@book_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Retrieves a single book by its ID."""
    book = find_book(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book

# UPDATE Book (Partial Update)
@book_router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdateModel):
    """Updates fields of an existing book."""
    book_to_update = find_book(book_id)
    if book_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    update_data = book_update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
         book_to_update[key] = value
    return book_to_update

# DELETE Book
@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Deletes a book by its ID."""
    book_to_delete = find_book(book_id)
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    BOOKS.remove(book_to_delete)
    return None