from pydantic import BaseModel

class User(BaseModel):
    id: int|None = None
    fullname: str|None = None
    age: int|None = None
    number: str|None = None
    book_id: int|None = None

class Book(BaseModel):
    id: int|None = None
    title: str|None = None
    author: str|None = None
    category: str|None = None

class Order(BaseModel):
    user_id: int|None = None
    full_name: str|None = None
    order: str|None = None
    