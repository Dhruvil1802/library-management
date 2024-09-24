from pydantic import BaseModel, Field
from typing import List, Optional



class BookCategoryCreate(BaseModel):
    name: str 

class BookCategory(BookCategoryCreate):
    id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str 
    author: str 
    category_id: int 

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    category: Optional[BookCategory] = None

    class Config:
        orm_mode = True

class BookList(BaseModel):
    books: List[Book]

    class Config:
        orm_mode = True
