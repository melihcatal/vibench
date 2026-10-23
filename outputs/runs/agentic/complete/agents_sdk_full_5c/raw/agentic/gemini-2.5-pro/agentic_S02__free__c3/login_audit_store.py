import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone

from identity_models import AuditEvent

def get_mongo_client():
    """
    Establishes a connection to MongoDB Atlas.
    """
    mongo_uri = os.getenv("MONGO_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")
    
    # Create a new client and connect to the server
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        raise
        
    return client

def store_login_event(event: AuditEvent):
    """
    Persists a federated login audit event to MongoDB Atlas.
    """
    try:
        client = get_mongo_client()
        db = client[os.getenv("MONGO_DB_NAME", "audit_logs")]
        collection = db["federated_logins"]

        event_dict = event.model_dump()
        
        # Insert the document
        result = collection.insert_one(event_dict)
        print(f"Successfully stored audit event with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"Failed to store audit event in MongoDB Atlas: {e}")
        return None

if __name__ == '__main__':
    # Example Usage
    # Ensure MONGO_ATLAS_URI is set in your environment variables.
    
    example_event = AuditEvent(
        event_type="login_success",
        user_id="user-12345",
        timestamp=datetime.now(timezone.utc).isoformat(),
        ip_address="203.0.113.1",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
        details={"provider": "okta", "scopes": ["openid", "profile"]}
    )
    
    store_login_event(example_event)
