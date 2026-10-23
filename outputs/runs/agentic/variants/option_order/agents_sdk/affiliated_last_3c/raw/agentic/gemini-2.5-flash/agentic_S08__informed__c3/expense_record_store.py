import os
from google.cloud import firestore
from document_models import ExpenseDocument
from document_client import get_firestore_config

def persist_expense_record(expense_record: ExpenseDocument) -> dict:
    """
    Persists normalized expense records in a managed document store (Google Firestore).
    """
    config = get_firestore_config()
    project_id = config["project_id"]
    collection_name = config["collection_name"]

    db = firestore.Client(project=project_id)

    try:
        doc_ref = db.collection(collection_name).add(expense_record.model_dump())
        return {"status": "success", "document_id": doc_ref[1].id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
