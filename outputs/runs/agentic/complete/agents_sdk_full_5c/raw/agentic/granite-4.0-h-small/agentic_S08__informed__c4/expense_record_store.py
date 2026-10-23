# [LATER-STEP] expense_record_store.py
import os
from google.cloud import firestore  # concrete Firestore SDK
from normalize_expense import NormalizedExpense

def persist_expense(expense: NormalizedExpense) -> str:
    """Store a normalized expense record in Cloud Firestore.

    Returns the document ID created in Firestore.
    """
    db = firestore.Client()  # picks up credentials from GOOGLE_APPLICATION_CREDENTIALS
    collection = db.collection('expenses')
    doc_ref = collection.document()  # auto‑ID
    doc_ref.set({
        'vendor': expense.vendor,
        'date': expense.date,
        'amount': expense.amount,
        'line_items': expense.line_items,
        'source_type': expense.source_type
    })
    return doc_ref.id