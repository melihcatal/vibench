import os
from document_models import NormalizedExpense
from document_client import get_firestore_client

def persist_expense_record(expense_record: NormalizedExpense, config: dict = None) -> str:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    collection_name = config.get("collection_name", "expense_records")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    db = get_firestore_client(project_id)
    
    doc_ref = db.collection(collection_name).add(expense_record.dict())

    return doc_ref[1].id

def get_expense_record(record_id: str, config: dict = None) -> NormalizedExpense:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    collection_name = config.get("collection_name", "expense_records")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    db = get_firestore_client(project_id)

    doc_ref = db.collection(collection_name).document(record_id)
    doc = doc_ref.get()

    if doc.exists:
        return NormalizedExpense(**doc.to_dict())
    else:
        raise ValueError(f"No expense record found with ID: {record_id}")

def update_expense_record(record_id: str, updates: dict, config: dict = None):
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    collection_name = config.get("collection_name", "expense_records")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    db = get_firestore_client(project_id)
    doc_ref = db.collection(collection_name).document(record_id)
    doc_ref.update(updates)


def delete_expense_record(record_id: str, config: dict = None):
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    collection_name = config.get("collection_name", "expense_records")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    db = get_firestore_client(project_id)
    db.collection(collection_name).document(record_id).delete()
