# Twitter API

Backend App using FastAPI ⚡ and MongoDB 🍃

Look in the tags if you want the app without mongo, juts using JSON


## Database Configuration

- **Database:** You need to create a DB named **tweeter in your Mongo cluster and paste the URL in config/db.py**
- **Create the collections:** The collections are **tweets** and **users**, but you don’t need to create them, you can go to post a tweet and post a user and they will be created.
- **Database structure:** You can see their JSON structure in **schemas**.

---

## How to start the app

- Create virtual environment: `python3 -m venv venv`
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run the app: `python3 main.py`
- Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

