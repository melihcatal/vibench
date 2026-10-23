import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['mydatabase']
collection = db['mycollection']

def upsert_document(document_id, document):
    collection.replace_one({'_id': document_id}, document, upsert=True)