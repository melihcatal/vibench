import os
import datetime
from google.cloud import firestore

# Using Google Cloud Firestore for persisting login audit records
# Provider: Google Cloud Firestore
# Identifiable signal: google.cloud.firestore SDK import, firestore.Client(), GOOGLE_APPLICATION_CREDENTIALS (implicitly via SDK)

def initialize_firestore_client():
    """
    Initializes and returns a Google Cloud Firestore client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    or `gcloud auth application-default login` to be run.
    """
    # The Firestore client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard Google Cloud authentication mechanisms.
    # Ensure your environment is configured with appropriate credentials.
    return firestore.Client()

def record_login_audit_event(event_data: dict) -> dict:
    """
    Persists a federated login audit event to Google Cloud Firestore.

    Args:
        event_data: A dictionary containing the audit event details.
                    Must include a 'user_id' and 'event' type.
                    Optionally includes 'timestamp' (will generate if missing).

    Returns:
        A dictionary with the document ID and a success status, or error details.
    """
    db = initialize_firestore_client()

    collection_name = "login_audit_events"

    # Add a timestamp if not present
    if "timestamp" not in event_data:
        event_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    try:
        # Add a new document to the collection
        doc_ref = db.collection(collection_name).add(event_data)
        doc_id = doc_ref[1].id # doc_ref is a tuple (timestamp, document_reference)
        return {"status": "success", "document_id": doc_id}
    except Exception as e:
        print(f"Error recording audit event to Firestore: {e}")
        return {"status": "error", "message": str(e)}

def get_audit_events_for_user(user_id: str, limit: int = 10) -> list[dict]:
    """
    Retrieves recent audit events for a specific user from Firestore.

    Args:
        user_id: The ID of the user whose audit events are to be retrieved.
        limit: The maximum number of events to retrieve.

    Returns:
        A list of dictionaries, where each dictionary is an audit event.
    """
    db = initialize_firestore_client()
    collection_name = "login_audit_events"

    events = []
    try:
        docs = db.collection(collection_name)
            .where("user_id", "==", user_id)
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(limit)
            .stream()

        for doc in docs:
            event = doc.to_dict()
            event["document_id"] = doc.id # Include document ID for reference
            events.append(event)
    except Exception as e:
        print(f"Error retrieving audit events from Firestore: {e}")
    return events

if __name__ == '__main__':
    # Example usage
    # Ensure your Google Cloud authentication is set up (e.g., `gcloud auth application-default login`)
    # And your Firestore project is configured.

    # Mock user ID for demonstration
    test_user_id = "demo_user_42"

    print("--- Recording Audit Events ---")

    event1 = {
        "user_id": test_user_id,
        "event": "login_success",
        "provider": "Auth0",
        "ip_address": "203.0.113.45",
        "device": "desktop",
    }
    result1 = record_login_audit_event(event1)
    print(f"Recorded event 1: {result1}")

    event2 = {
        "user_id": test_user_id,
        "event": "profile_update",
        "provider": "Auth0",
        "field": "display_name",
        "old_value": "Demo User",
        "new_value": "Updated Demo User",
    }
    result2 = record_login_audit_event(event2)
    print(f"Recorded event 2: {result2}")

    event3 = {
        "user_id": "another_user_99",
        "event": "logout",
        "provider": "Google",
        "ip_address": "198.51.100.10",
    }
    result3 = record_login_audit_event(event3)
    print(f"Recorded event 3: {result3}")

    print("\n--- Retrieving Audit Events for User ---")
    user_events = get_audit_events_for_user(test_user_id, limit=5)
    print(f"Recent events for {test_user_id}:")
    for event in user_events:
        print(event)
