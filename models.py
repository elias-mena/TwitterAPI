# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional

# Pydantic
from pydantic import (
    BaseModel,
    EmailStr,
    Field
    )

# User Models


class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(
        ...,
        example="Jhon@doe.com"
    )


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example='password'
        )


class User(UserBase):
    first_name: str = Field(
        ...,
        title='First name',
        min_length=1,
        max_length=50,
        example="John"
    )
    last_name: str = Field(
        ...,
        title='Last name',
        min_length=1,
        max_length=50,
        example="Doe"
    )
    birth_date: Optional[date] = Field(
        default=None,
        title='Birth date',
        example='2021-01-01'
    )


class UserRegister(User, UserLogin):
    pass


# Tweets Model


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256,
        example='This is a tweet!'
    )
    created_at: datetime = Field(
        default=datetime.now(),
        title='Creation date',
        example='2020-01-01T00:00:00Z'
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        title='Last update date',
        example='2020-01-01T00:00:00Z'
    )
    by: User = Field(
        ...,
        title='User who created the tweet'
    )
