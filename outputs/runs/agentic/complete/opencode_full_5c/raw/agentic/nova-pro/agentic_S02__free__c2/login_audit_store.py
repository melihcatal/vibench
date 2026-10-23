import os
import json
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.get_database("login_audit")
collection = db.get_collection("audit_records")


def persist_audit_record(record: dict):
    collection.insert_one(record)


if __name__ == "__main__":
    record = {
        "user_id": "user1",
        "event_type": "login",
        "timestamp": "2023-01-01T12:00:00Z",
    }
    persist_audit_record(record)
