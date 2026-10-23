import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['test_database']
collection = db['test_collection']

def fetch_document(document_id):
    return collection.find_one({'_id': document_id})