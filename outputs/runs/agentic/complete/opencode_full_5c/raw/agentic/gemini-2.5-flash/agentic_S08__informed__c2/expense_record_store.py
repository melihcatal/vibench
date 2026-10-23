import os
from document_models import NormalizedExpense
from document_client import get_firestore_client


def persist_expense_record(expense_record: NormalizedExpense) -> str:
    """
    Persists normalized expense records in Google Firestore.
    Returns the document ID of the stored record.
    """
    client = get_firestore_client()
    collection_name = os.environ.get("FIRESTORE_COLLECTION_NAME", "expense_records")

    # Convert dataclass to dictionary for Firestore
    expense_dict = expense_record.__dict__.copy()
    # Firestore doesn't directly support dataclass objects or nested dataclasses
    # Convert LineItem objects to dictionaries
    if "line_items" in expense_dict and expense_dict["line_items"] is not None:
        expense_dict["line_items"] = [
            item.__dict__ for item in expense_dict["line_items"]
        ]

    doc_ref = client.collection(collection_name).add(expense_dict)
    return doc_ref[1].id  # doc_ref is a tuple (update_time, DocumentReference)
