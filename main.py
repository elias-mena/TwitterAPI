# Python
from uuid import UUID
from typing import (
    Dict,
    List
    )

# FastAPI
from fastapi import (
    FastAPI, # Class that contains the app
    status,
    Path,
    Body
    )
import uvicorn # Server where the app runs

# Models
from models import(
    UserBase,
    UserLogin,
    User,
    Tweet
    )

app = FastAPI()

# Path Operations

## Users

### Register a user
@app.post(
    path="/singup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
    )
def singup(user: User) -> User:
    pass

### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def login(user: User) -> User:
    pass

### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_all_users() -> List[User]:
    pass

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Get a User",
    tags=["Users"]
    )
def show_user(
    id: int = Path(
        ...,
        gt=0,
        title='User ID',
        description='The ID of the user to retrieve',
        example=1
        )
)-> User:
    pass

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
    )
def delete_user(
    id: int = Path(
        ...,
        gt=0,
        title='User ID',
        description='The ID of the user to delete',
        example=1
        )
)-> User:
    pass

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
    )
def update_user(
    id: int = Path(
        ...,
        gt=0,
        title='User ID',
        description='The ID of the user to update',
        example=1
        )
)-> User:
    pass

## Tweets

### Show  all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home() -> List[Tweet]:
    return {"Twitter API": "Working!"}

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post() -> Tweet:
    pass

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet()-> Tweet:
    pass

### Delete a tweet
@app.delete(
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
    pass

### Update a tweet
@app.put(
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
    pass

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)