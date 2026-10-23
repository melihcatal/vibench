import os
from pymongo import MongoClient


def store_audit_record(record):
    client = MongoClient(os.environ.get('MONGODB_ATLAS_URI', ''))
    db = client.get_default_database()
    return db.login_audit.insert_one(record).inserted_id
