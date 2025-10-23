# src/__init__.py
from fastapi import FastAPI

# Import the router instance you created in books/routes.py
from .books.routes import book_router

# Create the main FastAPI app instance
# Add title, version, description etc. for documentation
app = FastAPI(
    title="Bookly API",
    description="A simple Book review web service using FastAPI.",
    version="1.0.0"
)

# Include the book router into the main app
app.include_router(
    book_router,
    prefix="/api/v1/books", # All routes in book_router will start with this path
    tags=["Books"]         # Group these endpoints under "Books" in the docs
)

# You would include other routers here (e.g., for users, reviews) in a larger app
# from .users.routes import user_router
# app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])


# Optional: Add a root endpoint for basic check
@app.get("/api/v1", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Bookly API!"}