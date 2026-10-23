import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['mydatabase']
collection = db['mycollection']

def query_documents(field, value):
    return list(collection.find({field: value}))