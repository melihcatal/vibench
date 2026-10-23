import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from identity_models import AuditRecord

# MongoDB Atlas configuration
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://user:password@cluster.mongodb.net/mydb?retryWrites=true&w=majority")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "federated_login_audit")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "audit_records")

def persist_audit_record(record: AuditRecord) -> Dict[str, Any]:
    try:
        # Connect to MongoDB Atlas
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        collection = db[MONGODB_COLLECTION]

        # Insert the audit record
        result = collection.insert_one(record.__dict__)
        client.close()
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except ConnectionFailure as e:
        print(f"MongoDB connection error: {e}")
        return {"status": "error", "message": f"MongoDB connection error: {e}"}
    except Exception as e:
        print(f"Error persisting audit record: {e}")
        return {"status": "error", "message": str(e)}
