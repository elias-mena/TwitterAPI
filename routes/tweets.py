# Python
from typing import List

# Fast Api
from fastapi import (
    APIRouter,
    FastAPI, # Class that contains the app
    status,
    Path,
    Body
    )

# User Model
from models.user import User

# Tweet Model
from models.tweet import Tweet

# Data base conection
from config.db import db

# Classes to serialize Bsons to Dicts and Lists
from squemas.squemas import serializeDict, serializeList

# To manage the Bsons ids
from bson import ObjectId

tweets = APIRouter()

## Tweets

### Show  all tweets
@tweets.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home() -> List[Tweet]:
    """
    # Home

    This path operation shows all tweets in the app

    ## Parameters:
        -

    ## Returns a json list with the basic tweet information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - update_at: Optional[datetime]
        - by: User
    """
    pass


### Post a tweet
@tweets.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)) -> Tweet:
    """
    # Post a tweet

    This path operation post a tweet in the app

    ## Parameters:
        - Request body parameter
            - tweet: Tweet

    ## Returns a json list with the basic tweet information:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - update_at: Optional[datetime]
        - by: User
    """
    pass

### Show a tweet
@tweets.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet()-> Tweet:
    """
    Show a Tweet

    This path operation show if a tweet exist in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    pass

### Delete a tweet
@tweets.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(
        id: int = Path(
        ...,
        gt=0,
        title='Tweet ID',
        description='The ID of the tweet to delete',
        example=1
        )
)-> Tweet:
    """
    Delete a Tweet

    This path operation delete a tweet in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with deleted tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """


### Update a tweet
@tweets.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet(
        id: int = Path(
            ...,
            gt=0,
            title='Tweet ID',
            description='The ID of the tweet to update',
            example=1
            )
)-> Tweet:
    """
    Update Tweet

    This path operation update a tweet information in the app and save in the database

    Parameters:
    - tweet_id: UUID
    - contet:str

    Returns a json with:
        - tweet_id: UUID
        - content: str 
        - created_at: datetime 
        - updated_at: datetime
        - by: user: User
    """
