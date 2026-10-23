import os
import json
from google.cloud import firestore
from typing import Dict, Any
from identity_client import IdentityClient

# -------------- Google Firestore (Managed NoSQL) --------------
# Reference: service=Cloud Firestore
FIRESTORE_COLLECTION = "federated-login-audit"

firestore_client = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var


def store_audit_record(record: Dict[str, Any]) -> None:
    """
    Persist a federated-login audit event to Firestore.
    The record structure matches the AuditEvent dataclass.
    """
    # Simple schema: auto-ID, fields = event_id, user_id, event_type, timestamp, payload
    doc_ref = firestore_client.collection(FIRESTORE_COLLECTION).document()
    doc_ref.set(record)
    print(f"Stored audit record {doc_ref.id}: {json.dumps(record)}")


# Example usage
# audit = {
#     "event_id": "e123",
#     "user_id": "u456",
#     "event_type": "login",
#     "timestamp": "2024-01-01T12:00:00Z",
#     "payload": {"description": "Logged in via Cognito"}
# }
# store_audit_record(audit)
