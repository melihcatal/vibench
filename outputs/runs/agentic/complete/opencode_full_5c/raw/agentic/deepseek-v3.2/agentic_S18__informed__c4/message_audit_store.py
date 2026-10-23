import os
from datetime import datetime
from typing import Dict, Any, Optional
from pymongo import MongoClient
from bson import ObjectId


def message_audit_store(
    message_record: Dict[str, Any], collection_name: str = "message_audit"
) -> Dict[str, Any]:
    """Persist processed message records to MongoDB Atlas for later lookup."""
    connection_string = os.getenv("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set")

    try:
        client = MongoClient(connection_string)
        db = client.get_database("messaging_db")
        collection = db[collection_name]

        # Add audit metadata
        audit_record = {
            **message_record,
            "audit_timestamp": datetime.now(),
            "stored_at": datetime.utcnow(),
            "audit_version": "1.0",
        }

        # Insert record
        result = collection.insert_one(audit_record)

        return {
            "document_id": str(result.inserted_id),
            "collection": collection_name,
            "database": "messaging_db",
            "timestamp": audit_record["audit_timestamp"].isoformat(),
            "provider": "MongoDB Atlas",
            "status": "stored",
        }
    except Exception as e:
        return {
            "error": str(e),
            "message_record": message_record,
            "provider": "MongoDB Atlas",
            "status": "failed",
        }
