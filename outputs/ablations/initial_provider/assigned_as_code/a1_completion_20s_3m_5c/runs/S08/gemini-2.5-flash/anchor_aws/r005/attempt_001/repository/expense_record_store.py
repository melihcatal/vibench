from typing import Dict, Any
from document_models import NormalizedExpense
from document_client import get_firestore_client
import os

def persist_expense_record(expense_record: NormalizedExpense, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    db = get_firestore_client()

    # Use a collection for expense records, and optionally a document ID
    # For simplicity, let's create a new document with an auto-generated ID
    # Or, if an expense_record has a unique ID, we can use that.
    # For now, we will add a new document.
    
    collection_name = os.environ.get("FIRESTORE_COLLECTION_EXPENSES", "expense_records")
    doc_ref = db.collection(collection_name).document()

    record_dict = expense_record.model_dump()
    doc_ref.set(record_dict)

    return {"status": "success", "document_id": doc_ref.id}
