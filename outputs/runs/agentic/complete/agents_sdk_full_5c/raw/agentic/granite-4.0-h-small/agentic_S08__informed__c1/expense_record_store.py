import os
from typing import TypedDict
import json
from google.cloud import firestore
from document_models import ExpenseRecord

# Firestore persistor (demonstration purpose)

def expense_record_store(normalized: dict, original_file: str) -> None:
    # Initialise Firestore client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    db = firestore.Client()
    doc_ref = db.collection('Expenses').document(f"{original_file}_{normalized['date'].replace('-', '')}")
    # Store raw normalized dict as a sub‑document
    doc_ref.set({
        'provider': normalized.get('vendor') or normalized.get('merchant') or 'unknown',
        'date': normalized['date'],
        'total': normalized['total'],
        'normalized': json.dumps(normalized)
    })
    print(f'Persisted expense record {doc_ref.id} in Firestore.')
