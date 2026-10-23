import os
import datetime
from google.cloud import firestore

def store_audit_record(message_id: str, processed_data: dict, status: str):
    db = firestore.Client()
    
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    # For local development, you might need to run `gcloud auth application-default login`

    doc_ref = db.collection("message_audit").document(message_id)
    doc_ref.set({
        "message_id": message_id,
        "processed_data": processed_data,
        "status": status,
        "timestamp": datetime.datetime.now(datetime.timezone.utc)
    })
    print(f"Audit record for message {message_id} stored in Firestore.")
