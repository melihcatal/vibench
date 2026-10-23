import os
from pymongo import MongoClient

os.environ['MONGODB_ATLAS_URI'] = 'your-mongodb-atlas-uri'

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['message_audit']
collection = db['messages']

def store_message(message):
    collection.insert_one(message)