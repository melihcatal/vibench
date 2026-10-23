import os
import pymongo
from typing import Dict, Any
from datetime import datetime

def message_audit_store(record: Dict[str, Any]) -> str:
    """
    Persists processed message records for later lookup in MongoDB Atlas.
    """
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required.")
    
    client = pymongo.MongoClient(uri)
    db = client["message_audit"]
    collection = db["audits"]
    
    record["processed_at"] = datetime.utcnow().isoformat()
    result = collection.insert_one(record)
    
    return str(result.inserted_id)