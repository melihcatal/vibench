import os
from google.cloud import firestore
from document_models import NormalizedExpense
import json

def persist_expense_record(expense: NormalizedExpense) -> dict:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    db = firestore.Client(project=project_id)

    collection_name = "expense_records"

    try:
        # Convert dataclass to a dictionary for Firestore
        expense_dict = expense.__dict__
        # Firestore doesn't directly support dataclass objects or nested dataclasses
        # We need to convert LineItem dataclasses to dictionaries as well
        expense_dict["line_items"] = [item.__dict__ for item in expense.line_items]

        doc_ref = db.collection(collection_name).add(expense_dict)
        
        return {
            "status": "success",
            "document_id": doc_ref[1].id, # doc_ref is a tuple (timestamp, document_reference)
            "provider": "google_cloud_firestore"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "provider": "google_cloud_firestore"
        }
