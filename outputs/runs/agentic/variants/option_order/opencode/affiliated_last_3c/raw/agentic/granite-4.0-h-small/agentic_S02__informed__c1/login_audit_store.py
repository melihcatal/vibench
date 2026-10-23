import os
import json
from google.cloud import firestore

# Managed NoSQL document store example: Google Firestore

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env var")

# Initialize Firestore client
firestore_client = firestore.Client()
AUDIT_COLLECTION = "federated_login_audit"


def persist_audit_record(record: Dict[str, Any]) -> str:
    """Persist a single audit event to Firestore and return the generated document ID.

    The record is expected to contain at least:
        - user_id (string)
        - event_type (e.g., 'login_success', 'code_exchange_failed')
        - details (dict with free-form info)
        - timestamp (ISO string, optional; if omitted the server sets it)
    """
    doc_ref = firestore_client.collection(AUDIT_COLLECTION).document()
    doc_ref.set(record)
    return doc_ref.id


# Simple CLI for local testing
if __name__ == "__main__":
    demo_record = {
        "user_id": "demo_user_42",
        "event_type": "code_exchange_success",
        "details": {
            "access_token_expires_in": 3600,
            "scopes": ["openid", "profile", "email"],
        },
        "timestamp": "2025-08-22T12:34:56Z",
    }
    doc_id = persist_audit_record(demo_record)
    print("Persisted audit record ID:", doc_id)
