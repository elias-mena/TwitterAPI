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

## Home

app.get(path="/")
def home()-> Dict[str, str]:
    return {"Twitter API":"Working!"}

## Users

@app.post(
    path="/singup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
    )
def singup(user: User) -> User:
    pass


@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def login(user: User) -> User:
    pass


@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_all_users() -> List[User]:
    pass


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
        description='The ID of the user to retrieve',
        example=1
        )
    )-> User:
    pass

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
        description='The ID of the user to retrieve',
        example=1
        )
    )-> User:
    pass

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)