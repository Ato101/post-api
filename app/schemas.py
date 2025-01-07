from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title : str
    content : str


class PostCreate(PostBase):
    pass 


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        from_attributes = True


class Post(BaseModel):
    title: str
    content : str
    published : bool
    owner_id :int
    owner :UserResponse

    class Config:
        from_attributes =True



class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner_id: int
    owner :UserResponse
    vote: int

    class Config:
        orm_attributes = True  # Allows Pydantic to read from ORM models like SQLAlchemy

class PostListResponse(BaseModel):
    posts: list[PostResponse]

class UserCreate(BaseModel):
    email :EmailStr
    password :str



class Login(UserCreate):
    pass


class Token(BaseModel):
    access_token :str
    token_type:str

class TokenData(BaseModel):
    id :Optional[int] = None


class Vote(BaseModel):
    post_id :int
    dir:int=Field(strict=True,le=1)