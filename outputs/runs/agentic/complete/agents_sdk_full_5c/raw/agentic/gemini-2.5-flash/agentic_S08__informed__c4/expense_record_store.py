import os
from google.cloud import firestore
from document_models import ExpenseDocument

def persist_expense_record(expense_doc: ExpenseDocument, collection_name: str = "expense_records") -> str:
    """Persist normalized expense records in Google Cloud Firestore."""
    # Google Cloud Firestore automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or other standard authentication methods.
    db = firestore.Client()

    # Convert Pydantic model to dictionary
    expense_data = expense_doc.model_dump()

    # Add to a collection, Firestore will auto-generate a document ID
    doc_ref = db.collection(collection_name).add(expense_data)

    return doc_ref[1].id
