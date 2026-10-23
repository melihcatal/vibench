import os
import datetime
from pymongo import MongoClient
from identity_models import AuditEvent


def store_audit_event(event: AuditEvent):
    """
    Persists an audit event to a MongoDB Atlas cluster.
    """
    client = MongoClient(os.environ.get("MONGO_ATLAS_CONNECTION_STRING"))
    db = client.get_database("audit_logs")
    collection = db.get_collection("federated_logins")

    doc = {
        "eventType": event.event_type,
        "userId": event.user_id,
        "details": event.details,
        "timestamp": datetime.datetime.utcnow(),
    }

    return collection.insert_one(doc).inserted_id
