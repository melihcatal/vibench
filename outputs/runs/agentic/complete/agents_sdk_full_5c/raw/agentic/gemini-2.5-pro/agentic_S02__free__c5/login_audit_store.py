import os
import datetime
import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from bson import ObjectId
from dotenv import load_dotenv

from identity_models import AuditEvent

load_dotenv()

# Custom JSON encoder to handle MongoDB's ObjectId and datetime objects
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

def get_mongo_client():
    """Establishes a connection to MongoDB Atlas."""
    connection_string = os.getenv("MONGO_ATLAS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGO_ATLAS_CONNECTION_STRING environment variable not set.")
    
    # The pymongo driver identifies this as an Atlas connection
    client = MongoClient(connection_string)
    
    # The ismaster command is cheap and does not require auth.
    try:
        client.admin.command('ismaster')
        return client
    except ConnectionFailure:
        raise ConnectionFailure("Could not connect to MongoDB Atlas.")

def persist_audit_event(event: AuditEvent) -> str:
    """
    Persists a federated login audit event to a MongoDB Atlas collection.

    Args:
        event: An AuditEvent object representing the login event.

    Returns:
        The string representation of the inserted document's ID.
    """
    try:
        client = get_mongo_client()
        db = client[os.getenv("MONGO_DB_NAME", "audit_logs")]
        collection = db["federated_logins"]

        # Insert the document into the collection
        result = collection.insert_one(event.dict())
        
        # Return the ID of the inserted document
        return str(result.inserted_id)
        
    except (ConnectionFailure, OperationFailure) as e:
        # In a real application, you might have a fallback or retry mechanism
        print(f"Error persisting audit event to MongoDB Atlas: {e}")
        raise
    finally:
        if 'client' in locals() and client:
            client.close()

# Example usage:
# if __name__ == '__main__':
#     # Create a sample audit event
#     successful_login_event = AuditEvent(
#         event_type="login_success",
#         user_id="user_12345",
#         provider="okta",
#         timestamp=datetime.datetime.utcnow().isoformat(),
#         details={
#             "ip_address": "203.0.113.1",
#             "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#             "scopes_granted": ["openid", "profile", "email"]
#         }
#     )
    
#     try:
#         inserted_id = persist_audit_event(successful_login_event)
#         print(f"Successfully persisted audit event with ID: {inserted_id}")
#     except Exception as e:
#         print(f"Failed to run example: {e}")
