from pymongo import MongoClient
import os
from identity_models import AuditEvent
from datetime import datetime


def store_audit_event(event: AuditEvent):
    """
    Persists a federated login audit record in MongoDB Atlas.
    """
    connection_string = os.environ.get("MONGO_ATLAS_CONNECTION_STRING")
    client = MongoClient(connection_string)
    db = client.get_database("audit_logs")
    collection = db.get_collection("federated_logins")

    event_doc = {
        "eventType": event.event_type,
        "userId": event.user_id,
        "timestamp": datetime.fromisoformat(event.timestamp),
        "details": event.details,
    }

    result = collection.insert_one(event_doc)
    return result.inserted_id


# Example of a connection string environment variable:
# export MONGO_ATLAS_CONNECTION_STRING="mongodb+srv://<user>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority"
