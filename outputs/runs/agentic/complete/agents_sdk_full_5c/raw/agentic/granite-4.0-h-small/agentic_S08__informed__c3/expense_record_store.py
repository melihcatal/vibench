import json
from google.cloud import firestore
from document_models import NormalizedExpense

# Initialize Firestore client (credentials taken from GOOGLE_APPLICATION_CREDENTIALS env var)
firestore_client = firestore.Client()


def store_expense_record(record: NormalizedExpense) -> str:
    # Create a unique document ID (you could use vendor+date or Firestore auto-ID)
    doc_id = f"expense_{record.vendor or 'unknown'!s[:20]}_{record.date or '2024-01-01'}"
    doc_ref = firestore_client.collection("expenses").document(doc_id)
    doc_ref.set(record.__dict__)
    return doc_id
