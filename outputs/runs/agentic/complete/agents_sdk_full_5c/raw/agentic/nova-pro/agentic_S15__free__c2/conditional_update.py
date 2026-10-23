import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['mydatabase']
collection = db['mycollection']

def conditional_update(document_id, update, condition):
    collection.update_one({'_id': document_id}, {'$set': update}, condition)