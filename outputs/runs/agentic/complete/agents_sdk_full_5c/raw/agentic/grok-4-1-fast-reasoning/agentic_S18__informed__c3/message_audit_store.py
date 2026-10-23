import os
import pymongo
from typing import Dict, Any

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
client = pymongo.MongoClient(MONGODB_ATLAS_URI)
db = client["messaging_db"]
collection = db["audits"]

def store_processed_message(record: Dict[str, Any]) -> str:
    result = collection.insert_one(record)
    return str(result.inserted_id)
