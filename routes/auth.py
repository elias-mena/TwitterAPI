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
from models.user import(
    UserLogin,
    User,
    UserRegister,
    )

# Data base connection
from config.db import db

# Functions to serialize Bsons to Dicts and Lists
from schemas.schemas import serializeDict, serializeList

# Algorithm to encript the password
from passlib.hash import sha256_crypt

# To manage the Bsons ids
from bson import ObjectId

auth_router = APIRouter()


## Register a user
@auth_router.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Auth"]
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
        - password: str
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    user = user.dict() # UserRegister to dictionary

    # Confirming if the id or the email of the user is already registered
    if db.users.find_one({"user_id": user["user_id"] }) is None:
        if db.users.find_one({"email": user["email"] }) is None:
            # Casting data
            user["birth_date"] = str(user["birth_date"]) # date to string
            user["password"] = sha256_crypt.hash(user["password"]) # encript password
            del user['id']
            user['_id'] = str(ObjectId())
            _id = user['_id']

            # Inserting and returning the user by id (Mongo id)
            db.users.insert_one(user)
            return serializeDict(db.users.find_one({"_id": _id}))
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email already registered.'
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"¡There is already a registered user with that identification number!"
        )

## Login a user
@auth_router.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Auth"]
    )
def login(user: UserLogin = Body(...)) -> User:

    user = user.dict()
    # Searching in the db by email
    db_user = db.users.find_one({"email": user["email"] })

    # Confirming if the email is registered
    if db_user is not None:
        db_user = serializeDict(db_user) # Bson to dictionary

        if sha256_crypt.verify(user["password"], db_user["password"]): # Compares (password,hash)
            return db_user

        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Password does not match'
                )

    raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Does not exists a user with that email'
                )