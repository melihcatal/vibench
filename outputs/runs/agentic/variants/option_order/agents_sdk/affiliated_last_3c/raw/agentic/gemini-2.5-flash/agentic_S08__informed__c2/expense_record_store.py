import os
import datetime
from google.cloud import firestore
from document_models import NormalizedExpense

def persist_expense_record(expense: NormalizedExpense) -> str:
    """
    Persists normalized expense records in Google Cloud Firestore.

    Args:
        expense: The NormalizedExpense object to persist.

    Returns:
        The ID of the created document in Firestore.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # default credentials are configured for Google Cloud.
    # The client will automatically pick up credentials from the environment.
    db = firestore.Client()

    # Convert Pydantic model to dictionary, ensuring proper serialization for Firestore
    expense_dict = expense.dict()

    # Firestore handles datetime objects directly, but Pydantic might store ISO strings
    # Ensure transaction_date is stored as a proper Firestore timestamp if it's an ISO string
    if isinstance(expense_dict.get("transaction_date"), str):
        try:
            expense_dict["transaction_date"] = datetime.datetime.fromisoformat(expense_dict["transaction_date"])
        except ValueError:
            pass # Keep as string if not a valid isoformat

    # Add a timestamp for when the record was created
    expense_dict["created_at"] = firestore.SERVER_TIMESTAMP

    # Define the collection name
    collection_name = "expense_records"

    # Add a new document to the collection
    doc_ref = db.collection(collection_name).add(expense_dict)

    return doc_ref[1].id # doc_ref is a tuple (update_time, DocumentReference)
