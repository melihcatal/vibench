from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime
import os

def expense_record_store(record: dict) -> dict:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        return {"error": "Missing MONGODB_ATLAS_URI"}
    try:
        client = MongoClient(uri)
        db = client["expense_records"]
        collection = db["expenses"]
        if "created_at" not in record:
            record["created_at"] = datetime.utcnow().isoformat()
        result = collection.insert_one(record)
        return {"success": True, "inserted_id": str(result.inserted_id)}
    except PyMongoError as e:
        return {"error": str(e)}