import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['test_database']
collection = db['test_collection']

def upsert_document(document_id, document):
    collection.replace_one({'_id': document_id}, document, upsert=True)