import os
import json
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from messaging_models import AuditRecord

def get_mongo_client():
    """Initializes and returns a MongoClient connected to MongoDB Atlas."""
    uri = os.getenv("MONGO_ATLAS_URI")
    if not uri:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")
        
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        raise
        
    return client

def store_audit_record(record: AuditRecord):
    """
    Persists a processed message audit record to a MongoDB Atlas collection.
    """
    client = get_mongo_client()
    db = client.get_database("message_audit_db")
    collection = db.get_collection("processed_messages")
    
    # Convert Pydantic model to dict for storage
    record_dict = record.dict()
    record_dict["timestamp"] = datetime.utcnow() # Add processing timestamp
    
    insert_result = collection.insert_one(record_dict)
    print(f"Stored audit record with ID: {insert_result.inserted_id}")
    client.close()
    return insert_result.inserted_id

if __name__ == '__main__':
    if os.getenv("MONGO_ATLAS_URI"):
        sample_record = AuditRecord(
            message_id="pubsub-message-id-12345",
            subscription_path="projects/my-project/subscriptions/my-sub",
            publish_time="2023-10-27T10:00:00Z",
            data={"customer_id": "C-987", "message": "Your package has arrived."},
            processing_outcome="SUCCESS",
            summary="Package arrival notification sent.",
            is_safe=True,
            translation="Tu paquete ha llegado."
        )
        store_audit_record(sample_record)
    else:
        print("Set MONGO_ATLAS_URI to run this example.")
        print("Example URI: mongodb+srv://<user>:<password>@<cluster-url>/?retryWrites=true&w=majority")
