from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config: # This is to convert the sqlalchemy model to pydantic model to return the data as per the Post schema
        # orm_mode = True
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional [int]


class Vote(BaseModel):
    post_id: int
    # dir: conint(le=1)
    dir: int