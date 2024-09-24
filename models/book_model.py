from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class BookCategory(Base):
    __tablename__ = "book_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), unique=True, index=True)

    books = relationship("Book", back_populates="category")
    

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255), index=True)
    author = Column(String(length=255))
    category_id = Column(Integer, ForeignKey("book_categories.id"))

    category = relationship("BookCategory", back_populates="books")
    borrowed_books = relationship("BorrowedBook", back_populates="book")