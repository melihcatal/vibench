import os
from typing import Any, Dict

from google.cloud import firestore

from document_models import normalize_expense_record


def expense_record_store(record: Any) -> Dict[str, Any]:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    client = firestore.Client(project=project_id)
    normalized = normalize_expense_record(record if isinstance(record, dict) else {"raw": record})
    doc_ref = client.collection("expense_records").document()
    doc_ref.set(normalized)
    return {"stored": True, "document_id": doc_ref.id, "record": normalized}
