from fastapi import FastAPI,Header,status,HTTPException
from typing import Optional,List
from src.books.schema import BookCreateModel,Book,BookUpdateModel

app=FastAPI()

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

@app.get('/')
async def read_root():
    return { 'message':'hello world!'}

@app.get('/greet')
async def greet_name(name:Optional[str]= 'User', age:int=0):
    return {"message": f"Hello {name}", "age": age}

#HELPER FUNCTION
def find_book(book_id:int):
    for book in BOOKS:
        if book["id"]==book_id:
            return book
        return None
        
@app.get('/books',response_model=List[Book])  
async def get_books(): 
    return BOOKS


@app.post('/books',response_model=Book,status_code=status.HTTP_201_CREATED)
async def create_book(book_data:BookCreateModel):
    new_book=book_data.model_dump()
    BOOKS.append(new_book)
    
    return new_book
   
# READ SINGLE Book
@app.get("/book/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Retrieves a single book by its ID."""
    book = find_book(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book 

#update existing
@app.patch("/books/{book_id}",response_model=Book)
async def update_book(book_id:int,book_update_data=BookUpdateModel):
    book_to_update=find_book(book_id)
    if book_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    update_data=book_update_data.model_dump(exclude_unset=True)
    # Update the book dictionary
    for key, value in update_data.items():
         book_to_update[key] = value

    return book_to_update

# DELETE Book
@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Deletes a book by its ID."""
    book_to_delete = find_book(book_id)
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    BOOKS.remove(book_to_delete)
    # No return needed for 204 status code
    return None # Or return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.get('/headers')
async def get_headers(
    accept:Optional[str]=Header(None),
    content_type: Optional[str]=Header(None,alias="Content-Type"),
    user_agent:Optional[str]=Header(None,alias="User-Agent"),
    host:Optional[str]=Header(None)
):
    request_headers={
        'accept':accept,
        'content_type':content_type,
        'user_agent':user_agent,
        'host':host
    }
    return request_headers