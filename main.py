# Python
import json
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
    UserRegister,
    Tweet
    )

# App

app = FastAPI()


# Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
    )
def signup(user: UserRegister = Body(...)) -> User:
    """
    # Signup

    This path operation register a user in the app

    ## Parameters:
        -Request body parameter
            - user: UserRegister

    ## Returns a json with the basic user information:
        - user_id: UUID
        - email: Emailsrt
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        # load the json list
        results = json.load(f)

        # convert the user (body) to a dictionary
        user_dict = user.dict()

        # casting user atributes
        user_dict["user_id"] = str(user_dict["user_id"]) # uuid to string
        user_dict["birth_date"] = str(user_dict["birth_date"]) # date to string

        # add the modified user
        results.append(user_dict)
        # move to the first byte of the file
        f.seek(0)
        # Save the changes in the json file
        json.dump(results,f)
    return user

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
    """
    # Show all users

    This path operation shows al users in the app

    ## Parameters:
        -

    ## Returns a json list with all users in the app, with the following keys:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.load(f)

        for user in results:
            user["user_id"] = UUID(user["user_id"])
        return results

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
    """
    Show a User

    This path operation show if a person exist in the app

    Parameters:
        - user_id: UUID

    Returns a json with user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(user_id)
    for data in results:
        if data["user_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡This user_id doesn't exist!"
        )

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
    """
    Delete a User

    This path operation delete a user in the app

    Parameters:
        - user_id: UUID

    Returns a json with deleted user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(user_id)
    for data in results:
        if data["user_id"] == id:
            results.remove(data)
            with open("users.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user_id doesn't exist!"
        )

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
    """
    Update User

    This path operation update a user information in the app and save in the database

    Parameters:
    - user_id: UUID
    - Request body parameter:
        - **user: User** -> A user model with user_id, email, first name, last name, birth date and password

    Returns a user model with user_id, email, first_name, last_name and birth_date
    """
    user_id = str(user_id)
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    with open("users.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
    for user in results:
        if user["user_id"] == user_id:
            results[results.index(user)] = user_dict
            with open("users.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user_id doesn't exist!"
        )


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
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.load(f)

        for tweet in results:
            tweet["tweet_id"] = UUID(tweet["tweet_id"])
            tweet["by"]["user_id"] = UUID(tweet["by"]["user_id"])
        return results

### Post a tweet
@app.post(
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
    with open("tweets.json", "r+", encoding="utf-8") as f:
        # load the json list
        results = json.load(f)

        # convert the tweet (body) to a dictionary
        tweet_dict = tweet.dict()

        # casting tweet atributes
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"]) # uuid to string
        tweet_dict["created_at"] = str(tweet_dict["created_at"]) # datetime to string
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"]) # datetime to string
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"]) # uuid to string
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"]) # date to string

        # add the modified tweet
        results.append(tweet_dict)
        # move to the first byte of the file
        f.seek(0)
        # save the changes in the json file
        json.dump(results,f)
    return tweet

### Show a tweet
@app.get(
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
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡This tweet_id doesn't exist!"
        )

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
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            results.remove(data)
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet_id doesn't exist!"
        )

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
    tweet_id = str(tweet_id)
    # tweet_dict = tweet.dict()
    # tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    # tweet_dict["birth_date"] = str(tweet_dict["birth_date"])
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
    for tweet in results:
        if tweet["tweet_id"] == tweet_id:
            tweet['content'] = content
            tweet['updated_at'] = str(datetime.now())
            print(tweet)
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet_id doesn't exist!"
        )

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)