from sqlalchemy.orm import Session
from models import book_model
from schemas import book_schemas


def create_book_category(db: Session, book_category: book_schemas.BookCategoryCreate):
    new_category = book_model.BookCategory(name=book_category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_book_categories(db: Session):
    return db.query(book_model.BookCategory).all()

def get_book_category(db: Session, category_id: int):
    return db.query(book_model.BookCategory).filter(book_model.BookCategory.id == category_id).first()

def update_book_category(db: Session, category_id: int, book_category: book_schemas.BookCategoryCreate):
    category = get_book_category(db, category_id)
    if not category:
        return None

    category.name = book_category.name
    db.commit()
    db.refresh(category)
    return category

def delete_book_category(db: Session, category_id: int):
    category = get_book_category(db, category_id)
    if not category:
        return False

    db.delete(category)
    db.commit()
    return True




def create_book(db: Session, book: book_schemas.BookCreate):
    category = db.query(book_model.BookCategory).filter(book_model.BookCategory.id == book.category_id).first()
    if not category:
        return None
    
    new_book = book_model.Book(
        title=book.title,
        author=book.author,
        category_id=book.category_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_books_by_category(db: Session,category_id):
    return db.query(book_model.Book).filter(book_model.Book.category_id == category_id).all()


def get_book(db: Session, book_id: int):
    return db.query(book_model.Book).filter(book_model.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book: book_schemas.BookCreate):
    existing_book = get_book(db, book_id)
    if not existing_book:
        return None

    category = db.query(book_model.BookCategory).filter(book_model.BookCategory.id == book.category_id).first()
    if not category:
        return None

    existing_book.title = book.title
    existing_book.author = book.author

    existing_book.category_id = book.category_id
    db.commit()
    db.refresh(existing_book)
    return existing_book


def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        return False

    db.delete(book)
    db.commit()
    return book
