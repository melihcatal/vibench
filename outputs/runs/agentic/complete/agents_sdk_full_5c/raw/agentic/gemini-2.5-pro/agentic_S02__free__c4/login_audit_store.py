import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Get MongoDB Atlas connection string from environment variable
MONGO_ATLAS_URI = os.environ.get("MONGO_ATLAS_URI")

if not MONGO_ATLAS_URI:
    raise ValueError("MONGO_ATLAS_URI environment variable not set.")

# Create a new client and connect to the server
# The use of 'mongodb+srv://' indicates a likely connection to a cloud provider like Atlas
client = MongoClient(MONGO_ATLAS_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB Atlas!")
    db = client.audit_logs
    login_events_collection = db.login_events
except Exception as e:
    print(e)
    # Fallback for demonstration if connection fails
    login_events_collection = None

def store_login_event(user_id: str, provider: str, success: bool, ip_address: str):
    """
    Persists a federated login audit record to a MongoDB Atlas collection.

    Args:
        user_id: The unique identifier for the user.
        provider: The identity provider (e.g., 'okta', 'google').
        success: Boolean indicating if the login was successful.
        ip_address: The source IP address of the login attempt.
    """
    if not login_events_collection:
        print("MongoDB collection not available. Cannot store event.")
        return

    event_document = {
        "userId": user_id,
        "provider": provider,
        "success": success,
        "ipAddress": ip_address,
        "timestamp": datetime.utcnow()
    }
    
    try:
        result = login_events_collection.insert_one(event_document)
        print(f"Successfully stored login event with id: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"Failed to store login event in MongoDB Atlas: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    store_login_event(
        user_id="user-12345",
        provider="okta",
        success=True,
        ip_address="203.0.113.1"
    )
    store_login_event(
        user_id="user-67890",
        provider="google",
        success=False,
        ip_address="198.51.100.2"
    )
