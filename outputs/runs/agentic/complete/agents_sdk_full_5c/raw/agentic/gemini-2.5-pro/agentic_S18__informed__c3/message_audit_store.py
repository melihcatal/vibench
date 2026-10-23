
import os
import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def get_db_client():
    """
    Returns a MongoClient connected to MongoDB Atlas.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")
    
    client = MongoClient(uri)
    
    # The ismaster command is cheap and does not require auth.
    try:
        client.admin.command('ismaster')
        return client
    except ConnectionFailure as e:
        print(f"MongoDB Atlas connection failed: {e}")
        raise

def store_message_audit(record: dict):
    """
    Persists a processed message record to a MongoDB Atlas collection.
    """
    client = None
    try:
        client = get_db_client()
        db = client.get_database("message_audits")
        collection = db.get_collection("processed_messages")
        
        # Add a timestamp to the record
        record_to_insert = record.copy()
        record_to_insert["processed_at"] = datetime.datetime.now(datetime.timezone.utc)
        
        result = collection.insert_one(record_to_insert)
        print(f"Successfully stored audit record with ID: {result.inserted_id}")
        return result.inserted_id
    except (ConnectionFailure, OperationFailure) as e:
        print(f"Failed to store audit record in MongoDB: {e}")
        return None
    finally:
        if client:
            client.close()

if __name__ == '__main__':
    # This is an example, not part of the required functionality.
    if os.getenv("MONGODB_ATLAS_URI"):
        sample_record = {
            "message_id": "msg-xyz-789",
            "status": "success",
            "content_length": 128,
            "analysis": {
                "is_safe": True,
                "summary": "A positive customer review."
            }
        }
        store_message_audit(sample_record)
