# Python
from typing import List
from datetime import datetime

# Fast Api
from fastapi import (
    APIRouter,
    FastAPI,
    status,
    HTTPException,
    Path,
    Body,
    Query
    )

# User Model
from models.user import User

# Tweet Model
from models.tweet import Tweet

# Data base connection
from config.db import db

# Classes to serialize Bsons to Dicts and Lists
from squemas.squemas import serializeDict, serializeList

# To manage the Bsons ids
from bson import ObjectId

tweets_router = APIRouter()

## Tweets Routes

### Show  all tweets
@tweets_router.get(
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
        - _id: str
        - content: str
        - created_at: datetime
        - update_at: Optional[datetime]
        - by: User
    """
    return serializeList(db.tweets.find())


### Post a tweet
@tweets_router.post(
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
        - _id: str
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    tweet = tweet.dict() # Tweet to dictionary

    tweet['updated_at'] = tweet['created_at']

    tweet["by"]["birth_date"] = str(tweet["by"]["birth_date"]) # date to string

    # To manage Mongo ids
    tweet["by"]["_id"] = tweet["by"]["id"]
    del tweet["by"]['id']
    del tweet['id']
    tweet['_id'] = str(ObjectId())

    _id = tweet['_id']

    # Inserting and returning the user by id
    db.tweets.insert_one(tweet)
    return serializeDict(db.tweets.find_one({"_id": _id}))


### Show a tweet
@tweets_router.get(
    path="/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(
    tweet_id : str = Path(
        ...,
        title='Tweet Id',
        description='Mongo ObjectId',
        example= f'{ObjectId()}'
        )
)-> Tweet:
    """
    # Show a Tweet

    This path operation show if a tweet exist in the app

    ## Parameters:
        - _id: str

    ## Returns a json with tweet data:
        - _id: str
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    tweet = db.tweets.find_one({"_id": tweet_id})
    if tweet is not None:
        return serializeDict(tweet)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡Doest not exist a tweet with that _id!"
        )


### Delete a tweet
@tweets_router.delete(
    path="/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(
    tweet_id : str = Path(
        ...,
        title='Tweet Id',
        description='Mongo ObjectId',
        example= f'{ObjectId()}'
        )
)-> Tweet:
    """
    # Delete a Tweet

    This path operation delete a tweet in the app

    ## Parameters:
        - _id: str

    ## Returns a json with deleted tweet data:
        - _id: str
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    tweet = db.tweets.find_one({"_id": tweet_id})
    if tweet is not None:
        return serializeDict(db.tweets.find_one_and_delete({"_id": tweet_id }))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡Doest not exist a tweet with that _id!"
        )


### Update a tweet
@tweets_router.put(
    path="/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet(
    tweet_id : str = Path(
        ...,
        title='Tweet Id',
        description='Mongo ObjectId',
        example= f'{ObjectId()}'
        ),
    content: str = Query(
        ...,
        min_length=1,
        max_length=256,
        example='This is a tweet!'
        )
)-> Tweet:
    """
    # Update Tweet

    This path operation update a tweet information in the app and save in the database

    ## Parameters:
        - _id: str
        - content:str

    ## Returns a json with:
        - _id: str
        - content: str
        - created_at: datetime
        - updated_at: datetime
        - by: user: User
    """
    tweet = db.tweets.find_one({"_id": tweet_id })

    if tweet is not None:
            tweet = serializeDict(tweet) # Bson to dictionary

            # Filter and set for the Mongo update
            filtr = {"_id": tweet_id }
            st = {"$set": {"content":content,"updated_at":datetime.now()}}
            db.tweets.update_one(filtr,st)

            return serializeDict(db.tweets.find_one({"_id": tweet_id }))


    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡Doest not exist a tweet with that identification number!"
        )
