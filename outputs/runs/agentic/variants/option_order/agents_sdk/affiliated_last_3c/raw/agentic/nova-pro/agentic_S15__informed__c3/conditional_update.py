import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['test_database']
collection = db['test_collection']

def conditional_update(document_id, update, condition):
    collection.update_one({'_id': document_id, **condition}, {'$set': update})