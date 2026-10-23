from google.cloud import firestore
import os
from typing import Dict, Any

def persist_expense_record(record: Dict[str, Any], collection_name: str = "expense_records") -> str:
    """
    Persists normalized expense records in Google Cloud Firestore.
    Returns the ID of the newly created document.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        return "Error: GOOGLE_CLOUD_PROJECT environment variable not set for Firestore."

    # Initialize Firestore DB client
    db = firestore.Client(project=project_id)

    try:
        # Add a new document to the specified collection
        doc_ref = db.collection(collection_name).add(record)
        return doc_ref[1].id # doc_ref is a tuple (update_time, DocumentReference)
    except Exception as e:
        return f"Error persisting expense record to Firestore: {e}"
