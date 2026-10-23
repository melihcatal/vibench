import os
from google.cloud import firestore
from datetime import datetime
from typing import Dict, Any

# Initialize Google Firestore client
# This assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or credentials are otherwise configured for the environment.
db = firestore.Client()

FIRESTORE_COLLECTION_NAME = os.environ.get("FIRESTORE_COLLECTION_NAME", "federated_login_audits")

def store_audit_record(record: Dict[str, Any]) -> str:
    """Persists a federated-login audit record in Google Firestore."""
    if not record.get("event_id"): # Ensure a unique ID for the document
        record["event_id"] = f"audit-{datetime.now().isoformat().replace('.', '-')}"
    
    # Ensure timestamp is present or set it
    if "timestamp" not in record:
        record["timestamp"] = datetime.utcnow().isoformat() + "Z"

    try:
        doc_ref = db.collection(FIRESTORE_COLLECTION_NAME).document(record["event_id"])
        doc_ref.set(record)
        print(f"Stored audit record with ID: {record['event_id']} in collection: {FIRESTORE_COLLECTION_NAME}")
        return record["event_id"]
    except Exception as e:
        print(f"Error storing audit record in Firestore: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    example_audit_record = {
        "event_id": "audit-login-001",
        "user_id": "user-123",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": "LOGIN_SUCCESS",
        "provider": "Auth0",
        "details": {
            "ip_address": "203.0.113.45",
            "device": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        },
        "session_id": "sess-abc-xyz"
    }
    stored_id = store_audit_record(example_audit_record)
    print(f"\n--- Firestore Audit Store Result ---")
    print(f"Attempted to store audit record. Result ID/Error: {stored_id}")

    example_audit_record_no_id = {
        "user_id": "user-456",
        "event_type": "TOKEN_REFRESH",
        "provider": "Google",
        "details": {"old_access_token_prefix": "ya29.", "new_access_token_prefix": "ya29.", "scope": "openid email"}
    }
    stored_id_auto = store_audit_record(example_audit_record_no_id)
    print(f"Attempted to store audit record (auto ID). Result ID/Error: {stored_id_auto}")
