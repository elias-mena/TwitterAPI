# Mongo Client
from pymongo import MongoClient

# Connection to the Mongo cluster
conn = MongoClient("mongodb+srv://user:password@cluster.evwck.mongodb.net/")


# Database
db = conn.tweeter

