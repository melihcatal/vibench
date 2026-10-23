import os
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
db = client["mydatabase"]
