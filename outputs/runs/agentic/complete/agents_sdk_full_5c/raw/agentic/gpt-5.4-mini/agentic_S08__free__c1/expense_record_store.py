import os
from typing import Any, Dict

from google.cloud import firestore

PROVIDER = "google_firestore"
FIRESTORE_PROJECT_ID_ENV = "GOOGLE_CLOUD_PROJECT"


def expense_record_store(record: Dict[str, Any], collection_name: str = "expense_records") -> str:
    project_id = os.getenv(FIRESTORE_PROJECT_ID_ENV)
    client = firestore.Client(project=project_id) if project_id else firestore.Client()
    doc_ref = client.collection(collection_name).document()
    doc_ref.set(record)
    return doc_ref.id
