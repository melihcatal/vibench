import os
from google.cloud import firestore
from document_models import NormalizedExpense


def persist_expense_record(expense_record: NormalizedExpense) -> str:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    db = firestore.Client()

    # Collection name can be dynamic or static based on your design
    collection_name = "expense_records"

    doc_ref = db.collection(collection_name).add(expense_record.dict())
    return doc_ref[1].id  # Returns the ID of the newly created document
