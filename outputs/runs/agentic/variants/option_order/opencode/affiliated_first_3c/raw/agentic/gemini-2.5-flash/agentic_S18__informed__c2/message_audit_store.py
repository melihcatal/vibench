import os
import datetime

from google.cloud import firestore

from messaging_models import MessageAuditStoreRequest, MessageAuditStoreResponse

# Google Cloud Firestore client will pick up credentials automatically if
# GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
# if running in a Google Cloud environment.


def persist_message_record(
    request: MessageAuditStoreRequest,
) -> MessageAuditStoreResponse:
    db = firestore.Client()

    # Define the collection name for audit records
    collection_name = "message_audit_records"

    doc_ref = db.collection(collection_name).document(request.message_id)

    # Prepare the data to be stored
    record_data = {
        "message_id": request.message_id,
        "payload": request.payload,
        "status": request.status,
        "timestamp": request.timestamp,  # Use the provided timestamp
        "stored_at": firestore.SERVER_TIMESTAMP,  # Firestore will add its own server timestamp
    }

    doc_ref.set(record_data)

    return MessageAuditStoreResponse(success=True)


if __name__ == "__main__":
    # Example Usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set up)
    message_id = "unique_message_id_12345"
    payload = {"user_id": "user_abc", "action": "login", "ip_address": "192.168.1.1"}
    status = "processed"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    request = MessageAuditStoreRequest(
        message_id=message_id, payload=payload, status=status, timestamp=timestamp
    )
    response = persist_message_record(request)

    if response.success:
        print(f"Message audit record for ID '{message_id}' persisted successfully.")
    else:
        print(f"Failed to persist message audit record for ID '{message_id}'.")
