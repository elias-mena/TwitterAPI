# Python
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
    #id:
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
    user_id : int = Field(
        ...,
        title='User Identification Number',
        gt=1,
        example="123456789123")
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