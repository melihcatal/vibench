# [LATER-STEP] expense_record_store.py
# Persists normalized expense records in Google Firestore (NoSQL document store)

import os
import firebase_admin
from firebase_admin import credentials, firestore
from document_models import normalize_record, InvoiceResponse

# Path to service account key JSON (should be set in environment)
FIRESTORE_CRED_PATH = os.getenv("FIRESTORE_SERVICE_ACCOUNT")

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIRESTORE_CRED_PATH)
firebase_admin.initialize_app(credential=cred)

db = firestore.client()

EXPENSE_COLLECTION = "expenses"


def store_expense(record: Dict[str, Any]) -> str:
    """Insert a normalized expense document into Firestore and return its document ID."""
    # Ensure the record follows the canonical schema
    normalized = normalize_record(record)
    # Generate a unique ID (UUID could be used; here we let Firestore auto-ID)
    doc_ref = db.collection(EXPENSE_COLLECTION).document()
    doc_ref.set(normalized)
    return doc_ref.id


def batch_store_expenses(records: List[Dict[str, Any]]) -> List[str]:
    """Efficiently store many expense records in a batch write."""
    batch = db.batch()
    ids = []
    for rec in records:
        doc_ref = db.collection(EXPENSE_COLLECTION).document()
        batch.set(doc_ref, normalize_record(rec))
        ids.append(doc_ref.id)
    batch.commit()
    return ids


if __name__ == "__main__":
    # Demo using a dummy normalized record (normally comes from pipeline)
    dummy_record = {
        "vendor": "Acme Corp",
        "date": "2024-09-01",
        "total": 123.45,
        "line_items": [
            {"description": "Widget", "quantity": 2, "total": 90.0},
            {"description": "Gadget", "quantity": 1, "total": 33.45},
        ],
        "merchant": "Corner Store",
        "tax": 8.9,
    }
    print("Stored expense doc ID:", store_expense(dummy_record))
