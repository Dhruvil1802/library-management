
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BorrowedBookBase(BaseModel):
    book_id: int
    borrower_id: int
    return_date: datetime

class BorrowedBookCreate(BaseModel):
    book_id: int

class BorrowedBook(BorrowedBookBase):
    id: int
    borrowed_on: datetime

    class Config:
        orm_mode = True

class ReturnBookRequest(BaseModel):
    borrowed_book_id: int