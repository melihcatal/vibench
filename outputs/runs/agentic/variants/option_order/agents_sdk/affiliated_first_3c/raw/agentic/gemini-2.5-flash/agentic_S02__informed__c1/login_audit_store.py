import os
import datetime
from google.cloud import firestore
from typing import Dict, Any
from identity_models import AuditEvent

# Configure Google Cloud Firestore
# This assumes GOOGLE_APPLICATION_CREDENTIALS is set in the environment
# or a service account key file is otherwise discoverable by the client.

def get_firestore_client():
    """Returns a Firestore client instance."""
    # Project ID can be automatically determined from the environment
    # if GOOGLE_CLOUD_PROJECT environment variable is set or credentials include it.
    return firestore.Client()

def persist_audit_event(event: AuditEvent) -> str:
    """Persists a federated-login audit record in Google Firestore."""
    db = get_firestore_client()
    collection_ref = db.collection("login_audit_events") # Firestore collection name

    # Convert AuditEvent dataclass to a dictionary for Firestore
    event_data = event.__dict__
    # Ensure timestamp is in a Firestore-compatible format (e.g., datetime object)
    if isinstance(event_data.get("timestamp"), str):
        try:
            event_data["timestamp"] = datetime.datetime.fromisoformat(event_data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            # Fallback if not ISO format, or handle error
            pass

    try:
        doc_ref = collection_ref.document(event.event_id)
        doc_ref.set(event_data)
        return f"Audit event {event.event_id} stored successfully in Firestore."
    except Exception as e:
        return f"Error storing audit event {event.event_id} in Firestore: {e}"

def get_audit_event(event_id: str) -> Optional[AuditEvent]:
    """Retrieves an audit event from Firestore by ID."""
    db = get_firestore_client()
    collection_ref = db.collection("login_audit_events")
    doc_ref = collection_ref.document(event_id)

    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        # Convert timestamp back to string if needed for AuditEvent constructor
        if isinstance(data.get("timestamp"), datetime.datetime):
            data["timestamp"] = data["timestamp"].isoformat()
        return AuditEvent(**data)
    return None

if __name__ == "__main__":
    # Example usage
    test_event = AuditEvent(
        event_id="audit_12345",
        timestamp=datetime.datetime.utcnow().isoformat() + "Z",
        user_id="testuser@example.com",
        event_type="login_success",
        ip_address="192.0.2.1",
        user_agent="TestClient/1.0",
        details={
            "provider": "Google Identity Platform",
            "method": "OAuth2",
            "session_id": "xyz789"
        }
    )

    # To run this example, ensure you have Google Cloud authentication set up (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # and the 'google-cloud-firestore' library installed. Also, a Firestore database must be active in your project.

    # Persist the event
    print(persist_audit_event(test_event))

    # Retrieve the event
    retrieved_event = get_audit_event("audit_12345")
    if retrieved_event:
        print("\nRetrieved Event:")
        print(retrieved_event)
    else:
        print("\nEvent not found.")
