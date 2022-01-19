# Python
from typing import List

# Fast Api
from fastapi import (
    APIRouter,
    FastAPI, # Class that contains the app
    status,
    HTTPException,
    Path,
    Body
    )

# User Models
from models.user import(
    UserBase,
    UserLogin,
    User,
    UserRegister,
    )

# Data base conection
from config.db import db

# Classes to serialize Bsons to Dicts and Lists
from squemas.squemas import serializeDict, serializeList

# To manage the Bsons ids
from bson.objectid import ObjectId

# Algorithm to hash the password
from passlib.hash import sha256_crypt

users = APIRouter()

## Users

### Register a user
@users.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
    )
def signup(user: UserRegister = Body(...)):
    """
    # Signup

    This path operation register a user in the app

    ## Parameters:
        -Request body parameter
            - user: UserRegister

    ## Returns a json with the basic user information:
        - user_id: int
        - email: Emailsrt
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    user = user.dict()
    user["birth_date"] = str(user["birth_date"]) # date to string
    user["password"] = sha256_crypt.encrypt(user["password"])
    if serializeDict(db.users.find_one({"user_id": user["user_id"] })) is None:
        id = db.users.insert_one(user).inserted_id
        return serializeDict(db.users.find_one({"_id": id}))
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡There is already a registered user with that identification number!"
        )

### Login a user
@users.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def login(user: User) -> User:
    pass

### Show all users
@users.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_all_users():
    """
    # Show all users

    This path operation shows al users in the app

    ## Parameters:
        -

    ## Returns a json list with all users in the app, with the following keys:
        - user_id: int
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    return serializeList(db.users.find())

### Show a user
@users.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Get a User",
    tags=["Users"]
    )
def show_user(
    user_id : int = Path(
        ...,
        gt=0,
        title='User ID',
        description='The ID of the user to retrieve',
        example=1
        )
)-> User:
    """
    # Show a User

    This path operation show if a person exist in the app

    ## Parameters:
        - user_id: int

    ## Returns a json with user data:
        - user_id: int
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    #user_id = str(user_id)
    return serializeDict(db.users.find_one({"user_id": user_id }))

### Delete a user
@users.delete(
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
        - user_id: int

    Returns a json with deleted user data:
        - user_id: int
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    pass

### Update a user
@users.put(
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
    - user_id: int
    - Request body parameter:
        - **user: User** -> A user model with user_id, email, first name, last name, birth date and password

    Returns a user model with user_id, email, first_name, last_name and birth_date
    """
    pass



### Register a user
@users.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
    )
def signup(user: UserRegister = Body(...)):
    """
    # Signup

    This path operation register a user in the app

    ## Parameters:
        -Request body parameter
            - user: UserRegister

    ## Returns a json with the basic user information:
        - email: Emailsrt
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    #if db.create_user(user):
        #return user
    pass
