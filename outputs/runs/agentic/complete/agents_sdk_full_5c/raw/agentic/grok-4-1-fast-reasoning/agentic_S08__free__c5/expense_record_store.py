import os
from google.cloud import firestore
from typing import Dict, Any
from document_models import NormalizedExpense

def expense_record_store(expense: Dict[str, Any], collection_name: str = 'expenses') -> str:
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    db = firestore.Client(project=project_id)
    normalized = NormalizedExpense(**expense)
    _, doc_ref = db.collection(collection_name).add(normalized.model_dump())
    return doc_ref.id