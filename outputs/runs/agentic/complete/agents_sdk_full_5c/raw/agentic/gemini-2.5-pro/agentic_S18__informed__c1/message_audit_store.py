import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def persist_audit_record(record: Dict[str, Any]):
    """
    Persists a processed message record to MongoDB Atlas for auditing.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    try:
        client = MongoClient(uri)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB Atlas: {e}")
        raise

    try:
        db = client.get_database("message_audit_db")
        collection = db.get_collection("processed_messages")
        insert_result = collection.insert_one(record)
        print(f"Persisted audit record with ID: {insert_result.inserted_id}")
        return insert_result.inserted_id
    except OperationFailure as e:
        print(f"Error persisting audit record to MongoDB Atlas: {e}")
        raise
    finally:
        client.close()
