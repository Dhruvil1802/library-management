
# from typing import List
# from authorization.student_authorization import get_current_user
# from crud import book_crud
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from schemas import book_schemas
# from schemas.book_borrowed_schemas import BorrowedBookCreate
# from crud.book_borrowed_crud import borrow_book, get_borrowed_book, return_book
# from models.student_model import Student

# router = APIRouter()


# # Borrow a book for the current user
# @router.post("/borrow/")
# def borrow_book_route(borrow_data: BorrowedBookCreate, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
#     result = borrow_book(db=db, borrow_data=borrow_data, current_user=current_user.student_id)
#     if not result:
#         raise HTTPException(status_code=400, detail="Unable to borrow book")
#     return result


# # Return a borrowed book for the current user
# @router.post("/return/{borrowed_book_id}")
# def return_book_route(borrowed_book_id: int, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
#     return return_book(db=db, borrowed_book_id=borrowed_book_id)


# # Get a list of books borrowed by the current user
# @router.get("/borrowedbook")
# def get_borrowed_book_route(db: Session = Depends(get_db),  current_user: Student = Depends(get_current_user)):
#     return get_borrowed_book(db=db, student_id = current_user.student_id)

# # Fetch a list of all books with pagination (skip and limit)
# @router.get("/fetchbook/{book_id}", response_model=book_schemas.Book)
# def get_book(book_id: int, db: Session = Depends(get_db),current_user: Student = Depends(get_current_user)):
#     book = book_crud.get_book(db=db, book_id=book_id)
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return book

# # Fetch a specific book by its category ID
# @router.get("/fetchbookslist/{category_id}", response_model=List[book_schemas.Book])
# def get_book(category_id: int, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
#     book = book_crud.get_books_by_category(db=db, category_id=category_id)
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return book


from typing import List
from authorization.student_authorization import get_current_user
from crud import book_crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import book_schemas
from schemas.book_borrowed_schemas import BorrowedBookCreate, ReturnBookRequest
from crud.book_borrowed_crud import borrow_book, get_borrowed_book, return_book
from models.student_model import Student

router = APIRouter()

# Borrow a book for the current user
@router.post("/borrow/")
def borrow_book_route(borrow_data: BorrowedBookCreate, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
    print("Current user ID:", current_user.student_id)
    result = borrow_book(db=db, borrow_data=borrow_data, current_user=current_user.student_id)
    if not result:
        raise HTTPException(status_code=400, detail="Unable to borrow book")
    return result

# Return a borrowed book for the current user
# @router.post("/return/")
# def return_book_route(borrowed_book_id: int, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
#     result = return_book(db=db, borrowed_book_id=borrowed_book_id, student_id=current_user.student_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Borrowed book not found or cannot be returned")
#     return result

@router.post("/return/")
def return_book_route(
    return_data: ReturnBookRequest,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    result = return_book(db=db, borrowed_book_id=return_data.borrowed_book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Borrowed book not found or cannot be returned")
    return result

# Get a list of books borrowed by the current user
@router.get("/borrowedbook")
def get_borrowed_book_route(db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
    borrowed_books = get_borrowed_book(db=db, student_id=current_user.student_id)
    if not borrowed_books:
        raise HTTPException(status_code=404, detail="No borrowed books found")
    return borrowed_books

# Fetch a specific book by its ID
@router.get("/fetchbook/{book_id}", response_model=book_schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
    book = book_crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Fetch a list of books by category ID
@router.get("/fetchbookslist/{category_id}", response_model=List[book_schemas.Book])
def get_books_by_category(category_id: int, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
    books = book_crud.get_books_by_category(db=db, category_id=category_id)
    if not books:
        raise HTTPException(status_code=404, detail="No books found in this category")
    return books
