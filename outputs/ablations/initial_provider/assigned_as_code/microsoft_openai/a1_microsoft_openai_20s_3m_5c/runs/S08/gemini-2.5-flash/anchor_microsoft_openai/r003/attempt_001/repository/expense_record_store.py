import os
from typing import Dict, Any
from google.cloud import firestore


def persist_expense_record(normalized_expense: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", config.get("project_id"))

    if not project_id:
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID environment variable or config value.")

    db = firestore.Client(project=project_id)

    try:
        # Using the transaction_id as the document ID in Firestore
        doc_ref = db.collection('expense_records').document(normalized_expense['transaction_id'])
        doc_ref.set(normalized_expense)
        return {"status": "success", "document_id": normalized_expense['transaction_id']}
    except Exception as e:
        return {"status": "error", "message": f"Failed to persist expense record: {str(e)}"}
