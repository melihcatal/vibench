import os
from typing import Dict, Any
from google.cloud import firestore
from document_client import DocumentClients, PROJECT_ID
from document_models import NormalizedExpense
import datetime

# Firestore collection name for expense records
EXPENSE_COLLECTION_NAME = os.environ.get("FIRESTORE_EXPENSE_COLLECTION", "expense_records")

def persist_expense_record(expense_record: NormalizedExpense) -> Dict[str, Any]:
    """Persists normalized expense records in a managed document store (Google Cloud Firestore).

    Args:
        expense_record: The NormalizedExpense dataclass instance to persist.

    Returns:
        A dictionary with the document ID and status of the persistence operation.
    """
    db = DocumentClients.get_firestore_client()
    collection_ref = db.collection(EXPENSE_COLLECTION_NAME)

    # Convert dataclass to a dictionary for Firestore. Handle datetime objects.
    expense_dict = expense_record.__dict__.copy()

    # Convert datetime.date to ISO format string for Firestore compatibility
    if isinstance(expense_dict.get("transaction_date"), datetime.date):
        expense_dict["transaction_date"] = expense_dict["transaction_date"].isoformat()

    # Handle nested dataclasses (LineItem/NormalizedExpenseItem) if they exist
    # Firestore can handle nested dicts, so we convert them directly.
    if 'expense_items' in expense_dict:
        expense_dict['expense_items'] = [
            item.__dict__ for item in expense_dict['expense_items']
        ]

    try:
        # Add a new document to the collection
        doc_ref = collection_ref.add(expense_dict)
        return {"status": "success", "document_id": doc_ref[1].id}
    except Exception as e:
        print(f"Error persisting expense record to Firestore: {e}")
        return {"status": "error", "message": str(e)}
