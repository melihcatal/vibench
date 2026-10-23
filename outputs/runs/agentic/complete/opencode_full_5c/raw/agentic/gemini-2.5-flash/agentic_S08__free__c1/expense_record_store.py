import os
from google.cloud import firestore
from document_models import NormalizedExpense

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")


def get_firestore_client():
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID must be set as an environment variable.")
    return firestore.Client(project=PROJECT_ID)


def save_expense_record(expense_record: NormalizedExpense) -> str:
    client = get_firestore_client()
    collection_ref = client.collection("expense_records")

    # Convert Pydantic model to dictionary for Firestore
    record_data = expense_record.dict()

    # Add a timestamp for when the record was saved
    import datetime

    record_data["created_at"] = datetime.datetime.now(datetime.timezone.utc)

    doc_ref = collection_ref.add(record_data)
    return doc_ref[1].id  # Return the ID of the newly created document


def get_expense_record(record_id: str) -> NormalizedExpense:
    client = get_firestore_client()
    doc_ref = client.collection("expense_records").document(record_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return NormalizedExpense(**data)
    else:
        raise ValueError(f"No expense record found with ID: {record_id}")
