import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from identity_models import AuditEvent
from datetime import datetime

def store_audit_event(event: AuditEvent):
    """
    Persists a federated login audit record in a MongoDB Atlas collection.

    Requires MONGO_ATLAS_CONNECTION_STRING environment variable.
    Example: mongodb+srv://<user>:<password>@<cluster-url>/<dbname>
    """
    connection_string = os.environ.get("MONGO_ATLAS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGO_ATLAS_CONNECTION_STRING is not set.")

    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("MongoDB Atlas connection successful.")
    except ConnectionFailure as e:
        print(f"MongoDB Atlas connection failed: {e}")
        raise
        
    db = client.get_default_database()
    if not db:
        # Fallback to a default db name if not in connection string
        db = client["audit_logs"] 
        
    audit_collection = db["login_events"]

    result = audit_collection.insert_one(event.model_dump())
    
    print(f"Stored audit event with ID: {result.inserted_id}")
    client.close()
    return result.inserted_id

# Example usage pattern:
# if __name__ == '__main__':
#     test_event = AuditEvent(
#         event_type='login_success',
#         user_id='user-12345',
#         timestamp=datetime.utcnow().isoformat(),
#         ip_address='192.168.1.100',
#         details={'provider': 'okta', 'claims_requested': ['openid', 'profile']}
#     )
#     store_audit_event(test_event)
