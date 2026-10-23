import os
from google.cloud import firestore
from document_models import NormalizedExpense


def persist_expense_record(
    expense_record: NormalizedExpense, collection_name: str = "expense_records"
) -> str:
    """
    Persists normalized expense records in a Google Firestore managed document store.
    """
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set.
    db = firestore.Client()

    # Convert dataclass to dictionary for Firestore
    expense_dict = expense_record.__dict__
    # Convert LineItem dataclass objects within the list to dictionaries
    if "line_items" in expense_dict and expense_dict["line_items"]:
        expense_dict["line_items"] = [
            item.__dict__ for item in expense_dict["line_items"]
        ]

    doc_ref = db.collection(collection_name).add(expense_dict)
    return doc_ref[1].id  # Return the ID of the newly created document
