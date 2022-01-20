import uvicorn # Server where the app runs
from fastapi import FastAPI

# Routers
from routes.auth import auth_router
from routes.users import users_router
from routes.tweets import tweets_router


app = FastAPI()
app.include_router(tweets_router,prefix='/tweets')
app.include_router(users_router,prefix='/users')
app.include_router(auth_router,prefix='/auth')

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)