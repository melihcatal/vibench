from google.cloud import firestore
import os
from typing import Dict, Any

# Provider: Google Cloud Firestore
# Identifiable by: google.cloud.firestore, GOOGLE_APPLICATION_CREDENTIALS


def message_audit_store(message_data: Dict[str, Any]) -> str:
    db = firestore.Client()
    audit_ref = db.collection("message_audit")

    doc_ref = audit_ref.add(
        {**message_data, "processed_at": firestore.SERVER_TIMESTAMP}
    )

    return doc_ref[1].id
