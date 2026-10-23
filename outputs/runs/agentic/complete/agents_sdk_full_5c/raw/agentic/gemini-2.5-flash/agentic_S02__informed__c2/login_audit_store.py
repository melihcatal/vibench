import os
import datetime
from google.cloud import firestore
from identity_client import FIRESTORE_PROJECT_ID, FIRESTORE_COLLECTION_AUDIT
from identity_models import LoginAuditEvent

# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for the SDK to pick up credentials.
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

def get_firestore_client():
    """Initializes and returns a Google Cloud Firestore client."""
    if FIRESTORE_PROJECT_ID:
        return firestore.Client(project=FIRESTORE_PROJECT_ID)
    else:
        # If project ID is not explicitly set, Firestore client will try to infer from environment
        return firestore.Client()

def persist_audit_record(event: LoginAuditEvent) -> str:
    """
    Persists a federated-login audit record in Google Cloud Firestore.
    
    Args:
        event: The LoginAuditEvent object to store.
        
    Returns:
        The ID of the created document in Firestore.
    """
    db = get_firestore_client()
    collection_ref = db.collection(FIRESTORE_COLLECTION_AUDIT)

    # Convert LoginAuditEvent dataclass to a dictionary for Firestore
    # Firestore handles datetime objects directly.
    event_dict = {
        "user_id": event.user_id,
        "event_type": event.event_type,
        "timestamp": event.timestamp,
        "ip_address": event.ip_address,
        "user_agent": event.user_agent,
        "details": event.details
    }
    
    doc_ref = collection_ref.add(event_dict)
    return doc_ref[1].id # doc_ref is a tuple (update_time, DocumentReference)

def fetch_audit_records(user_id: Optional[str] = None, limit: int = 10) -> List[LoginAuditEvent]:
    """
    Fetches federated-login audit records from Google Cloud Firestore.
    
    Args:
        user_id: Optional. Filter records by a specific user ID.
        limit: The maximum number of records to fetch.
        
    Returns:
        A list of LoginAuditEvent objects.
    """
    db = get_firestore_client()
    collection_ref = db.collection(FIRESTORE_COLLECTION_AUDIT)
    
    query = collection_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)
    if user_id:
        query = query.where("user_id", "==", user_id)
        
    results = []
    for doc in query.stream():
        data = doc.to_dict()
        if data:
            results.append(
                LoginAuditEvent(
                    user_id=data.get("user_id"),
                    event_type=data.get("event_type"),
                    timestamp=data.get("timestamp"),
                    ip_address=data.get("ip_address"),
                    user_agent=data.get("user_agent"),
                    details=data.get("details", {})
                )
            )
    return results

if __name__ == "__main__":
    from datetime import datetime
    
    # Example usage:
    print(f"Using Firestore Project ID: {FIRESTORE_PROJECT_ID}")
    print(f"Using Firestore Collection: {FIRESTORE_COLLECTION_AUDIT}")

    # 1. Persist an audit record
    new_event = LoginAuditEvent(
        user_id="test-user-001",
        event_type="LOGIN_SUCCESS",
        timestamp=datetime.utcnow(),
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0",
        details={"provider": "Auth0", "session_id": "abcde12345"}
    )
    doc_id = persist_audit_record(new_event)
    print(f"Persisted audit event with ID: {doc_id}")

    new_event_2 = LoginAuditEvent(
        user_id="test-user-002",
        event_type="LOGOUT",
        timestamp=datetime.utcnow(),
        ip_address="192.168.1.101",
        user_agent="Chrome/110",
        details={"provider": "Auth0"}
    )
    doc_id_2 = persist_audit_record(new_event_2)
    print(f"Persisted audit event with ID: {doc_id_2}")

    # 2. Fetch audit records
    print("\nFetching all recent audit records:")
    recent_events = fetch_audit_records(limit=5)
    for event in recent_events:
        print(f"  User: {event.user_id}, Type: {event.event_type}, Time: {event.timestamp}, Details: {event.details}")

    print("\nFetching audit records for test-user-001:")
    user_events = fetch_audit_records(user_id="test-user-001")
    for event in user_events:
        print(f"  User: {event.user_id}, Type: {event.event_type}, Time: {event.timestamp}, Details: {event.details}")
