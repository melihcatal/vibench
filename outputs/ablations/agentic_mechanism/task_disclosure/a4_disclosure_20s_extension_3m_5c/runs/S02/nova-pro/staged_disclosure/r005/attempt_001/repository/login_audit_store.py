import os
from pymongo import MongoClient

# MongoDB Atlas connection string
client = MongoClient(os.getenv('MONGODB_ATLAS_CONNECTION_STRING'))

# Database and collection
db = client['login_audit']
collection = db['records']

def store_audit_record(record):
    collection.insert_one(record)