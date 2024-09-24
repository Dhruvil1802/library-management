
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.book_borrow_model import BorrowedBook
from schemas.book_borrowed_schemas import BorrowedBookCreate



def borrow_book(db: Session, borrow_data: BorrowedBookCreate, current_user):
  
    borrowed_on = datetime.utcnow()
    return_date = borrowed_on + timedelta(days=30)

    borrowed_book = BorrowedBook(
        book_id=borrow_data.book_id,
        borrower_id=current_user,
        borrowed_on=borrowed_on,
        return_date=return_date
    )
    db.add(borrowed_book)
    db.commit()
    db.refresh(borrowed_book)
    return borrowed_book

def return_book(db: Session, borrowed_book_id: int):
    borrowed_book = db.query(BorrowedBook).filter(BorrowedBook.id == borrowed_book_id).first()
    if borrowed_book:
        borrowed_book.returned_on = datetime.utcnow()
        db.commit()
        db.refresh(borrowed_book)
    return borrowed_book

def get_borrowed_book(db:Session, student_id: int):
    return db.query(BorrowedBook).filter(BorrowedBook.borrower_id == student_id).all()
