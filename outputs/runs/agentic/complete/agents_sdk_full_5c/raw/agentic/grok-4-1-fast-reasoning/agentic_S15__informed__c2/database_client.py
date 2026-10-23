import os
from pymongo import MongoClient

def get_mongo_client():
    uri = os.environ.get('MONGODB_ATLAS_URI')
    if not uri:
        raise ValueError('MONGODB_ATLAS_URI environment variable is required.')
    return MongoClient(uri)

def get_collection(database_name='testdb', collection_name='documents'):
    client = get_mongo_client()
    return client[database_name][collection_name]