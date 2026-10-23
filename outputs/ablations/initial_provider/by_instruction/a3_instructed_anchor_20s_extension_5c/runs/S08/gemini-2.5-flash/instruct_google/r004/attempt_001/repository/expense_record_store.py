import os
from typing import Dict, Any
import google.cloud.firestore as firestore

def persist_expense_record(expense_record: Dict[str, Any], collection_name: str = "expense_records") -> Dict[str, Any]:
    # Initialize Firestore DB client
    # The GOOGLE_CLOUD_PROJECT_ID environment variable should be set for the client to infer the project.
    firestore_client = firestore.Client()

    # Add a new document to the specified collection
    # Firestore automatically creates the collection and document if they don't exist.
    try:
        doc_ref = firestore_client.collection(collection_name).add(expense_record)
        return {
            "status": "success",
            "document_id": doc_ref[1].id, # doc_ref is a tuple (timestamp, document_reference)
            "message": f"Expense record persisted with ID: {doc_ref[1].id}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to persist expense record: {e}"
        }
