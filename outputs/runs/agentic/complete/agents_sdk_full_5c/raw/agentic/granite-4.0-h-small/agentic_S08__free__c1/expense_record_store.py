from typing import Dict
from google.cloud import firestore

def expense_record_store(doc_id: str, expense: Dict[str, any]) -> None:
    """
    Persist a normalized expense record into Firestore (Google Cloud NoSQL document store).
    """
    db = firestore.Client()
    doc_ref = db.collection("expenses").document(doc_id)
    doc_ref.set(expense)
