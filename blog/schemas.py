from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    username: str
    email: EmailStr
class UserCreate(UserBase):
    password: str


class UserAll(UserBase):
    id: int
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


class User(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: User

    class Config:
        orm_mode = True


class PostVotes(BaseModel):
    Post: Post
    votes: int


class UserValidate(UserBase):
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1, ge=0)
