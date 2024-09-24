
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models.book_model import Book  # Adjust the import path as necessary
from models.student_model import Student  # Adjust the import path as necessary

class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrower_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)  # Reference student_id
    borrowed_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=False)
    returned_on = Column(DateTime, nullable=True)


    book = relationship('Book', back_populates='borrowed_books')
    student = relationship('Student', back_populates='borrowed_books')
