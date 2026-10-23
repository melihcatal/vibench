import os
import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from typing import Dict, Any

from messaging_models import ProcessingResult

def store_audit_record(record: ProcessingResult):
    """
    Persists a processed message record to MongoDB Atlas for later lookup.

    Args:
        record: A ProcessingResult object containing details of the processed message.
    """
    connection_string = os.getenv("MONGO_ATLAS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGO_ATLAS_CONNECTION_STRING environment variable not set.")
    
    db_name = os.getenv("MONGO_DB_NAME", "messaging_audit")
    collection_name = os.getenv("MONGO_COLLECTION_NAME", "processed_messages")

    try:
        # Provider-identifying signal: pymongo.MongoClient connecting to mongodb+srv
        client = MongoClient(connection_string, app_name="message_audit_store")
        
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        
        db = client[db_name]
        collection = db[collection_name]
        
        record_doc = {
            "message_id": record.message_id,
            "status": record.status,
            "detail": record.detail,
            "processed_at": datetime.datetime.fromisoformat(record.timestamp),
            "audit_timestamp": datetime.datetime.utcnow()
        }
        
        insert_result = collection.insert_one(record_doc)
        print(f"Successfully inserted audit record with ID: {insert_result.inserted_id}")
        return insert_result.inserted_id

    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB Atlas: {e}")
        raise
    except OperationFailure as e:
        print(f"An operation failed on MongoDB Atlas: {e}")
        raise
    finally:
        if 'client' in locals() and client:
            client.close()
