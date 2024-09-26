from pydantic import BaseModel, Field, constr
from typing import List, Optional



class BookCategoryCreate(BaseModel):
    name: constr(min_length=1)

class BookCategory(BookCategoryCreate):
    id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: constr(min_length=1)
    author: constr(min_length=1) 
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
