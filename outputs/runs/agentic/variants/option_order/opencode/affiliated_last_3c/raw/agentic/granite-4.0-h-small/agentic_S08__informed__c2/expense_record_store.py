import json
import os
from google.cloud import firestore


def store_expense_record(normalized):
    # Initialize Firestore client using GOOGLE_APPLICATION_CREDENTIALS env variable
    db = firestore.Client()
    # Construct document ID (e.g., hash of vendor+date)
    doc_id = f"{normalized.get('vendor_or_merchant', '')}-{normalized.get('date', '')}-{normalized.get('total', '')}".replace(
        " ", "_"
    )
    # Save to collection 'expenses'
    expense_ref = db.collection("expenses").document(doc_id)
    expense_ref.set(normalized)
    print(f"Stored expense record: {doc_id}")
