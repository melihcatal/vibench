from google.cloud import firestore
import os
from typing import Dict, Any, Optional

def expense_record_store(record: Dict[str, Any], doc_id: Optional[str] = None) -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    db = firestore.Client(project=project_id)
    
    expenses_ref = db.collection("normalized_expenses")
    
    if doc_id:
        doc_ref = expenses_ref.document(doc_id)
        doc_ref.set(record)
        return doc_id
    else:
        doc_ref = expenses_ref.add(record)
        return doc_ref[1].id