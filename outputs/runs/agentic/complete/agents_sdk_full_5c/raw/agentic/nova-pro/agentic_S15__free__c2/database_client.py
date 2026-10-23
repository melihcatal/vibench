import os
from pymongo import MongoClient

def get_client():
    return MongoClient(os.getenv('MONGODB_ATLAS_URI'))

def get_database(client, db_name):
    return client[db_name]

def get_collection(db, collection_name):
    return db[collection_name]