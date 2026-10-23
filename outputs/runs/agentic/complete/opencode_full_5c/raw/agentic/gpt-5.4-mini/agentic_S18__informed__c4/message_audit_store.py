import os
from datetime import datetime

from pymongo import MongoClient


def persist_message_record(record):
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client.get_database(
        os.environ.get("MONGODB_ATLAS_DB", "messaging")
    ).get_collection("audit_records")
    record = dict(record)
    record["persisted_at"] = datetime.utcnow()
    result = collection.insert_one(record)
    return {"inserted_id": str(result.inserted_id)}
