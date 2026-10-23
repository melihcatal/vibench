import os
from typing import Dict, Any, Optional
from google.cloud import firestore
from document_models import NormalizedExpense

def get_firestore_client(project_id: str):
    """Initializes and returns a Google Cloud Firestore client."""
    return firestore.Client(project=project_id)

def persist_expense_record(
    normalized_expense: NormalizedExpense,
    project_id: str,
    collection_name: str = "expense_records",
    document_id: Optional[str] = None,
) -> Optional[str]:
    """Persists a normalized expense record to Google Cloud Firestore.
    Returns the ID of the created or updated document.
    """
    try:
        db = get_firestore_client(project_id)
        doc_ref = db.collection(collection_name).document(document_id) if document_id else db.collection(collection_name).document()

        # Convert Pydantic model to dictionary, excluding optional fields if None
        expense_dict = normalized_expense.dict(exclude_none=True)

        doc_ref.set(expense_dict)
        print(f"Expense record saved to Firestore with ID: {doc_ref.id}")
        return doc_ref.id

    except Exception as e:
        print(f"Error persisting expense record to Firestore: {e}")
        return None
