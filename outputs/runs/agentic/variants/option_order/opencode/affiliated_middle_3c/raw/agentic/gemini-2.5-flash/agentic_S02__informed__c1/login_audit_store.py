import os
import datetime
from google.cloud import firestore
from identity_models import AuditEvent
from typing import Dict, Any


def store_audit_record_firestore(event: AuditEvent) -> str:
    """
    Persists a federated login audit record in Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    # Google Cloud Firestore automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or the default gcloud credentials.
    # No explicit GOOGLE_APPLICATION_CREDENTIALS check here, as the client handles it.

    db = firestore.Client()
    collection_ref = db.collection("federated_login_audits")

    event_data = {
        "event_id": event.event_id,
        "timestamp": event.timestamp,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "details": event.details,
    }

    try:
        doc_ref = collection_ref.document(event.event_id)
        doc_ref.set(event_data)
        return f"Audit record {event.event_id} stored successfully in Firestore."
    except Exception as e:
        print(f"Error storing audit record in Firestore: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    # Example AuditEvent
    example_event = AuditEvent(
        event_id=f"audit_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        timestamp=datetime.datetime.now().isoformat(),
        user_id="test_user_789",
        event_type="LOGIN_ATTEMPT",
        details={
            "ip_address": "198.51.100.1",
            "status": "failed",
            "reason": "user_not_found",
        },
    )

    print(f"Storing audit event {example_event.event_id} in Firestore...")
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up (e.g., via gcloud auth application-default login)
    result = store_audit_record_firestore(example_event)
    print(result)

    # You can verify by checking your Firestore console under the collection "federated_login_audits"
