import os
from pymongo import MongoClient

def store_audit_record(record):
    client = MongoClient(os.environ['MONGODB_URI'])
    db = client['audit_db']
    collection = db['login_audit']
    collection.insert_one(record)