# Python
from typing import List

# Fast Api
from fastapi import (
    APIRouter,
    FastAPI,
    status,
    HTTPException,
    Path,
    Body
    )

# User Models
from models.user import User, UserRegister

# Data base connection
from config.db import db

# Functions to serialize Bsons to Dicts and Lists
from schemas.schemas import serializeDict, serializeList

# Algorithm to encript the password
from passlib.hash import sha256_crypt

users_router = APIRouter()

# Users Routes

## Show all users
@users_router.get(
    path="/",
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
        - _id: str
        - user_id: int
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    return serializeList(db.users.find())


## Show a user
@users_router.get(
    path="/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Get a User",
    tags=["Users"]
    )
def show_user(
    user_id : str = Path(
        ...,
        min_length=12,
        max_length=12,
        title='User ID',
        description='The ID of the user to retrieve',
        example="123456789123"
        )
)-> User:
    """
    # Show a User

    This path operation show if a person exist in the app

    ## Parameters:
        - user_id: int

    ## Returns a json with user data:
        - _id: str
        - user_id: int
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    user = db.users.find_one({"user_id": user_id })
    if user is not None:
        return serializeDict(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡Doest not exist a user with that identification number!"
        )


## Delete a user
@users_router.delete(
    path="/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
    )
def delete_user(
    user_id : str = Path(
        ...,
        min_length=12,
        max_length=12,
        title='User ID',
        description='The ID of the user to retrieve',
        example=123456789123
        )
)-> User:
    """
    # Delete a User

    This path operation delete a user in the app

    ## Parameters:
        - user_id: int

    ## Returns a json with deleted user data:
        - _id: str
        - user_id: int
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    user = db.users.find_one({"user_id": user_id })
    if user is not None:
        return serializeDict(db.users.find_one_and_delete({"user_id": user_id }))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡Doest not exist a user with that identification number!"
        )


## Update a user
@users_router.put(
    path="/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
    )
def update_user(
    user_id: str = Path(
        ...,
        min_length=12,
        max_length=12,
        title='User ID',
        description='The ID of the user to update',
        example="123456789123"
        ),
    user: UserRegister = Body(...)
)-> User:
    """
    # Update User

    This path operation update a user information in the app and save in the database

    ## Parameters:
        - user_id: int
        - Request body parameter:
            - **user: User

    ## Returns a json with user data:
        - _id: str
        - user_id: int
        - email: Emailstr
        - password: str
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """

    db_user = db.users.find_one({"user_id": user_id })

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡Doest not exist a user with that identification number!"
        )

    # Casting data
    db_user = serializeDict(db_user) # Bson to dictionary
    user = user.dict()  # User to dictionary
    user["birth_date"] = str(user["birth_date"]) # date to string

    # Validating email
    if db.users.find_one({"email": user["email"] }) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email already registered.'
            )

    # Verifying if the password changed
    if sha256_crypt.verify(user["password"], db_user["password"]): # Compares (password,hash)
        del user["password"]
    else:
        user["password"] = sha256_crypt.hash(user["password"]) # encript new password

    # Retrieving only the data that has changed
    del user["user_id"] # It never changes
    user = {key:value for (key,value) in user.items() if value != db_user[key]}

    # Filter and set for the Mongo update
    filtr = {"user_id": user_id }
    st = {"$set": user}
    db.users.update_one(filtr,st)

    return serializeDict(db.users.find_one({"user_id": user_id }))




