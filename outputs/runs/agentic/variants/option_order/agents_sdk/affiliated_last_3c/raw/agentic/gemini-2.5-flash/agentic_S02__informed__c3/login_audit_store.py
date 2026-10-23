import os
from google.cloud import firestore
from identity_models import AuditEvent
from datetime import datetime

def store_audit_event(event: AuditEvent, collection_name: str = "federated_login_audits") -> str:
    """
    Persists a federated-login audit record in Google Cloud Firestore.

    Args:
        event: The AuditEvent object to store.
        collection_name: The name of the Firestore collection to store events in.

    Returns:
        The ID of the document created in Firestore.
    """
    # Google Cloud Firestore client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or other standard authentication methods.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key.

    db = firestore.Client()

    # Convert AuditEvent dataclass to a dictionary for Firestore
    event_data = {
        "event_id": event.event_id,
        "user_id": event.user_id,
        "timestamp": datetime.fromisoformat(event.timestamp.replace("Z", "+00:00")), # Convert ISO string to datetime object
        "event_type": event.event_type,
        "ip_address": event.ip_address,
        "user_agent": event.user_agent,
        "metadata": event.metadata
    }

    # Add a document to the specified collection
    doc_ref = db.collection(collection_name).add(event_data)

    return doc_ref[1].id # doc_ref is (timestamp, DocumentReference)

def get_audit_event(doc_id: str, collection_name: str = "federated_login_audits") -> AuditEvent | None:
    """
    Retrieves an audit event from Google Cloud Firestore by its document ID.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        # Convert Firestore timestamp back to ISO string for AuditEvent
        if isinstance(data.get("timestamp"), datetime):
            data["timestamp"] = data["timestamp"].isoformat().replace("+00:00", "Z")
        return AuditEvent(
            event_id=data.get("event_id"),
            user_id=data.get("user_id"),
            timestamp=data.get("timestamp"),
            event_type=data.get("event_type"),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            metadata=data.get("metadata")
        )
    return None

if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # e.g., os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    # Ensure the Firestore project is initialized and has a database.

    new_event = AuditEvent(
        event_id="evt_firestore_123",
        user_id="user_firestore_456",
        timestamp=datetime.utcnow().isoformat() + "Z",
        event_type="login_success_persistent",
        ip_address="203.0.113.45",
        user_agent="Mozilla/5.0 ...",
        metadata={'auth_provider': 'Auth0', 'session_id': 'sess_abc'}
    )

    try:
        print(f"\nStoring audit event: {new_event.event_id}")
        document_id = store_audit_event(new_event)
        print(f"  Event stored with document ID: {document_id}")

        print(f"\nRetrieving event with ID: {document_id}")
        retrieved_event = get_audit_event(document_id)
        if retrieved_event:
            print(f"  Retrieved Event ID: {retrieved_event.event_id}, Type: {retrieved_event.event_type}")
            print(f"  Retrieved Event Timestamp (type): {type(retrieved_event.timestamp)}")
        else:
            print(f"  Event with ID {document_id} not found.")

    except Exception as e:
        print(f"Error with Firestore operations: {e}")
