import os
from pymongo import MongoClient

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")

client = MongoClient(MONGODB_ATLAS_URI)
db = client.get_database()


def store_audit_record(record):
    db.audit_records.insert_one(record)
