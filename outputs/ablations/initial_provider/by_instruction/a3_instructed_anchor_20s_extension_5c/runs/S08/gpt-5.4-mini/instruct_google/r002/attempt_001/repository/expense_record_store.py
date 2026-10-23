import os
from google.cloud import firestore


def expense_record_store(record: dict) -> str:
    client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc = client.collection("expense_records").document()
    doc.set(record)
    return doc.id
