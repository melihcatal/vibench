import os
from typing import Dict, Any, Optional

from google.cloud import firestore

from document_models import NormalizedExpense

def get_firestore_client():
    """Returns a Google Cloud Firestore client."""
    # https://cloud.google.com/firestore/docs/client/get-clients
    # It's recommended to set GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For local development, you might set it like:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    return firestore.Client()

def persist_expense_record(
    expense_record: NormalizedExpense,
    collection_name: str = "expense_records",
    document_id: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Persists a normalized expense record in Google Cloud Firestore."""

    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set as environment variable GOOGLE_CLOUD_PROJECT_ID.")

    db = get_firestore_client()

    # Convert NormalizedExpense dataclass to a dictionary for Firestore
    expense_data = expense_record.__dict__
    # Convert LineItem dataclasses to dictionaries
    if expense_data.get("line_items"):
        expense_data["line_items"] = [item.__dict__ for item in expense_data["line_items"]]

    if document_id:
        doc_ref = db.collection(collection_name).document(document_id)
    else:
        doc_ref = db.collection(collection_name).document()

    doc_ref.set(expense_data)

    return {"status": "success", "document_id": doc_ref.id}
