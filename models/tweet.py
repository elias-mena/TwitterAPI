# Python
from datetime import date, datetime
from typing import Optional,List

# Pydantic
from pydantic import BaseModel,Field

# User Model
from models.user import User

# To manage the Bsons ids
from bson import ObjectId

# Tweets Model

class Tweet(BaseModel):
    id : Optional[str] = Field(
        title='Mongo ObjectId',
        example= f'{ObjectId()}',
        alias="_id"
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
    content: str = Field(
        ...,
        min_length=1,
        max_length=256,
        example='This is a tweet!'
        )
    by: User = Field(
        ...,
        title='User who created the tweet'
        )


