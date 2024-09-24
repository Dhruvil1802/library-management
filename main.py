from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer


import logging

from routes import book_borrowed_routes, book_routes, lib_admin_routes, student_routes

from database import SessionLocal, engine, Base


logging.basicConfig(level=logging.DEBUG) 

Base.metadata.create_all(bind=engine)


app = FastAPI()



app.include_router(lib_admin_routes.router, tags=["Library Admin"])
app.include_router(student_routes.router, tags=["Student"])
app.include_router(book_routes.router,  tags=["books"])
app.include_router(book_borrowed_routes.router,  tags=["books"])
 




@app.get("/")
def read_root():
    logging.debug("Root endpoint hit")
    return {"message": "Welcome to the Library Management System"}