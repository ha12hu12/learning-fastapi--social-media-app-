from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from typing import Annotated
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)

class PostVote(BaseModel): #its for the vote showing when u get all posts
    Post: PostResponse
    votes: int

    model_config = ConfigDict(from_attributes=True)

class PostCreate(PostBase):
    pass

#--------------------Users---------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

#------------Token---------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

#------------Vote---------------

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]