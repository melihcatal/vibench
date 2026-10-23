import os
from typing import Any, Dict

from google.cloud import firestore


def expense_record_store(
    record: Dict[str, Any], collection_name: str = "expense_records"
) -> str:
    client = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc_ref = client.collection(collection_name).document()
    doc_ref.set(record)
    return doc_ref.id
