from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase): 
    pass


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)


    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    owner: UserResponse


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    post_dir: conint(le=1)


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    Post: PostResponse
    vote_count: int
