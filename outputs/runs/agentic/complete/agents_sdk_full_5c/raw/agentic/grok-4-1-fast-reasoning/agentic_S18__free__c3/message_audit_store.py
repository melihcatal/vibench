import os
import pymongo

MONGODB_URI = os.getenv("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URI)
db = client["messaging_audit"]
audits_collection = db["processed_messages"]

def store_audit_record(record_id: str, record: dict):
    audits_collection.update_one(
        {"_id": record_id},
        {"$set": record},
        upsert=True
    )