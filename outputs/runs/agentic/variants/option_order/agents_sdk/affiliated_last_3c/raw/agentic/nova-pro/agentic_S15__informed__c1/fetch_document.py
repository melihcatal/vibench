import os
from pymongo import MongoClient

MONGODB_ATLAS_URI = os.getenv('MONGODB_ATLAS_URI')

client = MongoClient(MONGODB_ATLAS_URI)
db = client['mydatabase']
collection = db['mycollection']

def fetch_document(document_id):
    return collection.find_one({'_id': document_id})