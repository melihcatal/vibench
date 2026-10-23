import os
from google.cloud import firestore
from typing import Dict

def expense_record_store(expense: Dict[str, Any]) -> None:
    """Persist the normalized expense record to Firestore."""
    db = firestore.Client()
    collection = db.collection("expenses")
    doc_id = expense.get("expense_id") or str(os.urandom(4).hex())
    collection.document(doc_id).set(expense)
    print(f"Stored expense {doc_id} in Firestore.")