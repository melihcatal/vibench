import os
from google.cloud import firestore
import json
from identity_client import get_firestore_config
from identity_models import LoginAuditEvent

def persist_audit_event(event: LoginAuditEvent):
    # Google Cloud Firestore uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # your environment is configured for Application Default Credentials.

    config = get_firestore_config()
    project_id = config["GOOGLE_PROJECT_ID"]
    collection_name = config["FIRESTORE_COLLECTION_NAME"]

    try:
        db = firestore.Client(project=project_id)
        doc_ref = db.collection(collection_name).document(event.event_id)
        doc_ref.set(event.to_dict())
        print(f"Successfully persisted audit event '{event.event_id}' to Firestore collection '{collection_name}' in project '{project_id}'.")
        return True
    except Exception as e:
        print(f"Error persisting audit event to Firestore: {e}")
        return False

if __name__ == "__main__":
    sample_event = LoginAuditEvent(
        event_id="evt_firestore_001",
        timestamp="2023-10-27T11:30:00Z",
        user_id="user_firestore_test",
        event_type="login_success",
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.111 Mobile Safari/537.36",
        status="success",
        details={"provider": "Google", "country": "US", "city": "Mountain View"}
    )
    
    print("Attempting to persist sample audit event:")
    success = persist_audit_event(sample_event)
    if success:
        print(f"Event '{sample_event.event_id}' was successfully stored.")
    else:
        print(f"Failed to store event '{sample_event.event_id}'. Check logs for details.")

    # Example of retrieving to verify (optional)
    # config = get_firestore_config()
    # project_id = config["GOOGLE_PROJECT_ID"]
    # collection_name = config["FIRESTORE_COLLECTION_NAME"]
    # db = firestore.Client(project=project_id)
    # doc_ref = db.collection(collection_name).document(sample_event.event_id)
    # doc = doc_ref.get()
    # if doc.exists:
    #     print("\nRetrieved event:")
    #     print(json.dumps(doc.to_dict(), indent=2))
    # else:
    #     print("\nEvent not found after persistence attempt.")
