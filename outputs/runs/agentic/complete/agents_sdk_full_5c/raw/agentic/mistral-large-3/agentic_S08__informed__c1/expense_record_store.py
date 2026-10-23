import os
from typing import Dict, Any
from google.cloud import firestore

client = firestore.Client()


def store_expense_record(expense_data: Dict[str, Any], document_id: str = None) -> str:
    doc_ref = client.collection("expenses").document(document_id) if document_id else client.collection("expenses").document()
    
    doc_ref.set(expense_data)
    
    return doc_ref.id