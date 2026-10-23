import os
from google.cloud import firestore
from document_models import NormalizedExpense
from typing import Union, Dict, Any


def expense_record_store(expense_data: Union[Dict[str, Any], NormalizedExpense]) -> str:
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    db = firestore.Client(project=project_id)
    if hasattr(expense_data, "model_dump"):
        record = expense_data.model_dump()
    else:
        record = expense_data
    _, doc_ref = db.collection("normalized_expenses").add(record)
    return doc_ref.id
