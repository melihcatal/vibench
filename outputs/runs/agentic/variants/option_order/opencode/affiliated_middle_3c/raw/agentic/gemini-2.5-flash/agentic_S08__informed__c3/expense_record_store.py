import os
from typing import Dict, Any
from google.cloud import firestore  # Provider identifiable import: Google Firestore
from document_models import NormalizedExpense

# Configure Google Firestore
# GOOGLE_APPLICATION_CREDENTIALS should be set in the environment.
# For local development, this typically points to a service account key file.
# In Google Cloud environments, credentials are automatically handled.

FIRESTORE_COLLECTION = os.environ.get("FIRESTORE_EXPENSE_COLLECTION", "expense_records")


def store_expense_record(expense: NormalizedExpense) -> Optional[str]:
    """
    Persists a normalized expense record in Google Firestore.
    This function is a scored component.
    """
    db = firestore.Client()

    # Convert Pydantic model to a dictionary suitable for Firestore
    # Handle date conversion for Firestore
    expense_dict = expense.model_dump()
    if isinstance(expense_dict.get("transaction_date"), str):
        # Firestore handles datetime objects directly, but pydantic might serialize to string
        # Ensure it's a date object before storing if possible, or Firestore will store as string.
        pass  # Firestore can usually handle ISO 8601 date strings if not converted to datetime objects

    try:
        # Add a new document to the collection
        doc_ref = db.collection(FIRESTORE_COLLECTION).add(expense_dict)
        return doc_ref[1].id  # Return the ID of the newly created document
    except Exception as e:
        print(f"Error storing expense record in Firestore: {e}")
        return None
