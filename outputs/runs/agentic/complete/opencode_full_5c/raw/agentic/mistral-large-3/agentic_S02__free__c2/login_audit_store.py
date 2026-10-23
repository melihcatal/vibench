import os
from typing import Dict, Any
from google.cloud import firestore

# Google Cloud Firestore Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
FIRESTORE_COLLECTION = "federated_login_audit"


def persist_audit_record(record: Dict[str, Any]) -> str:
    """Persist federated-login audit records in Google Cloud Firestore."""
    client = firestore.Client(project=GCP_PROJECT_ID)
    doc_ref = client.collection(FIRESTORE_COLLECTION).document()

    record["timestamp"] = firestore.SERVER_TIMESTAMP
    doc_ref.set(record)

    return doc_ref.id
