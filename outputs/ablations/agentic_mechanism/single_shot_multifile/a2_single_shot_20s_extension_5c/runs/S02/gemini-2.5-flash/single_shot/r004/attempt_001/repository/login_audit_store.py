import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

from identity_client import MONGODB_URI, MONGODB_DATABASE, MONGODB_COLLECTION
from identity_models import AuditRecord

def persist_audit_record(record: AuditRecord) -> Dict[str, Any]:
    """Persists a federated login audit record into a MongoDB Atlas document store."""
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI environment variable not set.")

    try:
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        collection = db[MONGODB_COLLECTION]
        
        # Convert dataclass to dictionary for MongoDB insertion
        record_dict = record.__dict__
        # Ensure datetime objects are stored correctly by PyMongo
        
        insert_result = collection.insert_one(record_dict)
        
        client.close()
        return {"acknowledged": insert_result.acknowledged, "inserted_id": str(insert_result.inserted_id)}
    except ConnectionFailure as e:
        raise ConnectionFailure(f"Could not connect to MongoDB Atlas: {e}") from e
    except OperationFailure as e:
        raise OperationFailure(f"MongoDB operation failed: {e}") from e
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}") from e
