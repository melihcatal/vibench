import os
import json
from google.cloud import datastore


def store_audit_record(record: Dict):
    """
    Persist a federated-login audit record to Google Cloud Firestore (NoSQL document store).
    Initialize Firestore client with GOOGLE_APPLICATION_CREDENTIALS env var.
    """
    client = datastore.Client()
    # Create an entity in the 'login_audit' collection
    key = client.key("login_audit")
    entity = datastore.Entity(key=key)
    entity.update(record)
    # Save to Firestore
    client.put(entity)
    print("Audit record stored with key:", entity.key.name)


# Simple CLI for local testing
if __name__ == "__main__":
    test_record = {
        "event_type": "login_success",
        "user_id": "u_12345",
        "provider": "microsoft",
        "timestamp": "2024-08-01T12:34:56Z",
        "details": {"ip": "203.0.113.5", "session_id": "sess_a1b2c3"},
    }
    store_audit_record(test_record)
