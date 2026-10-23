import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from messaging_models import AuditEvent

_client = None

def get_mongo_client():
    """Initializes and returns a MongoClient connection to MongoDB Atlas."""
    global _client
    if _client is None:
        mongo_uri = os.getenv("MONGO_ATLAS_URI")
        if not mongo_uri:
            raise ValueError("MONGO_ATLAS_URI environment variable not set.")
        
        _client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        try:
            _client.admin.command('ping')
            print("Successfully connected to MongoDB Atlas!")
        except Exception as e:
            print(f"Failed to connect to MongoDB Atlas: {e}")
            _client = None # Reset client on failure
            raise

    return _client

def store_audit_record(record: AuditEvent):
    """
    Persists a processed message audit record to MongoDB Atlas.

    Args:
        record: The AuditEvent object to store.
    """
    client = get_mongo_client()
    if not client:
        raise ConnectionError("Could not establish connection to MongoDB.")
        
    db_name = os.getenv("MONGO_DB_NAME", "messaging_audit")
    collection_name = os.getenv("MONGO_COLLECTION_NAME", "events")
    
    db = client[db_name]
    collection = db[collection_name]
    
    insert_result = collection.insert_one(record.dict())
    print(f"Stored audit record with ID: {insert_result.inserted_id}")
    return insert_result.inserted_id
