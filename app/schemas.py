from pydantic import BaseModel, EmailStr, conint
from typing import Optional, Tuple
from datetime import datetime
from typing import List


# User Schemas
class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    name: str
    pass


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # for Pydantic v2+


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# Post Schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse  # Related user information !!!

    class Config:
        from_attributes = True  # for Pydantic v2+


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class PostListWithVotes(BaseModel):
    Post: PostResponse
    votes: int


class PostListWithCounts(BaseModel):
    total_posts: int
    posts: List[PostListWithVotes]


# Vote Schema
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # direction can be 0 or 1
