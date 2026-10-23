import os
from typing import Any, Dict

from google.cloud import firestore


def expense_record_store(record: Dict[str, Any], collection: str = "expenses") -> str:
    client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc = client.collection(collection).document()
    doc.set(record)
    return doc.id
