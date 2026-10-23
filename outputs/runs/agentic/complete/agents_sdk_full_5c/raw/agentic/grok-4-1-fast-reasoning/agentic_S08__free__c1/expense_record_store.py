import os
from google.cloud import firestore
from document_models import NormalizedExpense
from typing import Dict, Any

def expense_record_store(expense: Dict[str, Any]) -> str:
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    db = firestore.Client(project=project_id)
    _, doc_ref = db.collection('expenses').add(expense)
    return doc_ref.id
