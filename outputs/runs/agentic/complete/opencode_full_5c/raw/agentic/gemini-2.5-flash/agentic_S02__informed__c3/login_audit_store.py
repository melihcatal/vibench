import os
import datetime
from google.cloud import firestore

# Google Firestore integration
# Provider-identifying signal: google.cloud.firestore and GOOGLE_APPLICATION_CREDENTIALS implicitly handled by SDK

db = firestore.Client()
AUDIT_COLLECTION = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "login_audit_records")


def record_audit_event(event_data: dict) -> dict:
    """Persists a federated-login audit record in Google Firestore."""
    try:
        # Add a timestamp if not present
        if "timestamp" not in event_data:
            event_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

        doc_ref = db.collection(AUDIT_COLLECTION).add(event_data)
        return {"status": "success", "document_id": doc_ref[1].id, "event": event_data}
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to record audit event in Firestore: {e}",
        }


def get_audit_events(limit: int = 10, user_id: str | None = None) -> list[dict]:
    """Retrieves recent federated-login audit records from Google Firestore."""
    try:
        query = db.collection(AUDIT_COLLECTION).order_by(
            "timestamp", direction=firestore.Query.DESCENDING
        )
        if user_id:
            query = query.where("user_id", "==", user_id)

        events = []
        for doc in query.limit(limit).stream():
            event = doc.to_dict()
            event["id"] = doc.id
            # Convert datetime objects to ISO format strings for easier serialization/display
            if "timestamp" in event and isinstance(
                event["timestamp"], datetime.datetime
            ):
                event["timestamp"] = event["timestamp"].isoformat()
            events.append(event)
        return events
    except Exception as e:
        print(f"Error fetching audit events from Firestore: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    print("\nRecording example audit event:")
    event = {
        "user_id": "user_test_123",
        "action": "login_success",
        "provider": "Google",
        "ip_address": "192.168.1.1",
        "details": {"session_id": "abc123xyz"},
    }
    record_result = record_audit_event(event)
    print(record_result)

    print("\nRetrieving recent audit events:")
    recent_events = get_audit_events(limit=3)
    for evt in recent_events:
        print(evt)

    print("\nRetrieving audit events for a specific user:")
    user_events = get_audit_events(limit=2, user_id="user_test_123")
    for evt in user_events:
        print(evt)
