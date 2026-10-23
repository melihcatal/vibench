import os
from pymongo import MongoClient

uri = os.getenv('MONGODB_ATLAS_URI')
client = MongoClient(uri)
db = client['mydatabase']
collection = db['messages']

def store_message(message):
    collection.insert_one(message)