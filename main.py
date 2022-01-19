import uvicorn # Server where the app runs
from fastapi import FastAPI
from routes.users import users
from routes.tweets import tweets

app = FastAPI()
app.include_router(users)
app.include_router(tweets)

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)