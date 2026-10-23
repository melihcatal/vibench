import json
import os
from messaging_models import AuditRecord

# Example: MongoDB Atlas (pymongo)
MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
client = None  # will be lazy-initialized


def init_store():
    global client
    if client is None:
        from pymongo import MongoClient

        client = MongoClient(MONGO_URI)
        db = client["messaging_audit"]
        return db["records"]
    return client["messaging_audit"]["records"]


def persist_record(record: AuditRecord):
    """Insert a processed message record into the NoSQL store."""
    collection = init_store()
    # Convert dataclasses to dict
    doc = {
        "timestamp": record.timestamp,
        "message_id": record.message_id,
        "payload": record.payload,
        "outcome": record.outcome,
    }
    collection.insert_one(doc)
