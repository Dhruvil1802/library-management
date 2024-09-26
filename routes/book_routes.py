from authorization.lib_admin_authorization import get_current_admin
from crud import book_crud
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from crud.book_crud import create_book_category
from models.lib_admin_model import LibAdmin
from schemas import book_schemas

router = APIRouter()

# Create a new book category
@router.post("/book-categories/", response_model=book_schemas.BookCategory, status_code=201)
def create_new_book_category(book_category: book_schemas.BookCategoryCreate, db: Session = Depends(get_db), current_user: LibAdmin = Depends(get_current_admin)):
    return create_book_category(db=db, book_category=book_category)

# Get a list of all book categories with pagination (skip and limit)
@router.get("/book-categories/", response_model=List[book_schemas.BookCategory])
def get_book_categories(db: Session = Depends(get_db),current_user: LibAdmin = Depends(get_current_admin)):
    return book_crud.get_book_categories(db=db)

# Fetch a specific book category by its ID
@router.get("/book-categories/{category_id}", response_model=book_schemas.BookCategory)
def get_book_category(category_id: int, db: Session = Depends(get_db),current_user: LibAdmin = Depends(get_current_admin)):
    category = book_crud.get_book_category(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Update a specific book category by its ID
@router.put("/book-categories/{category_id}", response_model=book_schemas.BookCategory)
def update_book_category(category_id: int, book_category: book_schemas.BookCategoryCreate, db: Session = Depends(get_db),current_user: LibAdmin = Depends(get_current_admin)):
    updated_category = book_crud.update_book_category(db=db, category_id=category_id, book_category=book_category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

# Delete a specific book category by its ID
@router.delete("/book-categories/{category_id}", status_code=204)   
def delete_book_category(category_id: int, db: Session = Depends(get_db),current_user: LibAdmin = Depends(get_current_admin)):
    result = book_crud.delete_book_category(db=db, category_id=category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return result

# Create a new book
@router.post("/books/", response_model=book_schemas.Book, status_code=201)
def create_book(book: book_schemas.BookCreate, db: Session = Depends(get_db),current_user: LibAdmin = Depends(get_current_admin)):
    new_book = book_crud.create_book(db=db, book=book)
    if not new_book:
        raise HTTPException(status_code=404, detail="Category not found")
    return new_book


# Get a list of all books with category_id (skip and limit)
@router.get("/booksbycategory/{category_id}", response_model=List[book_schemas.Book])
def get_books(category_id: int, db: Session = Depends(get_db), current_user: LibAdmin = Depends(get_current_admin)):
    
    books = book_crud.get_books_by_category(db=db, category_id=category_id)
    
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this category")
    
    return books

# Fetch a specific book by its ID
@router.get("/books/{book_id}", response_model=book_schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db),current_user: LibAdmin = Depends(get_current_admin)):
    book = book_crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update a specific book by its ID
@router.put("/books/{book_id}", response_model=book_schemas.Book)
def update_book(book_id: int, book: book_schemas.BookCreate, db: Session = Depends(get_db),current_user: LibAdmin = Depends(get_current_admin)):
    updated_book = book_crud.update_book(db=db, book_id=book_id, book=book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book     

# Delete a specific book by its ID
@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db),current_user: LibAdmin = Depends(get_current_admin)):
    result = book_crud.delete_book(db=db, book_id=book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return result