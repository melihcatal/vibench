import os

from google.cloud import firestore


def expense_record_store(record: dict):
    client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc_id = record.get("document_id") or record.get("id") or "expense_record"
    client.collection("expense_records").document(doc_id).set(record)
    return {"stored": True, "document_id": doc_id}
