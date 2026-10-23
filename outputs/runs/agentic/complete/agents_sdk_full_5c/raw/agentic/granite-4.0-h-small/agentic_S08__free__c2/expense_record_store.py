# [LATER-STEP] expense_record_store.py
"""
Persist normalized expense records in a managed document store using Google Firestore.
"""
import json
from google.cloud import firestore
from document_models import NormalizedExpense

def store_expense(record: NormalizedExpense) -> str:
    """Upload a normalized expense to Firestore collection 'expenses'.

    Args:
        record: Normalized expense payload.

    Returns:
        Document ID of the persisted record.
    """
    db = firestore.Client()  # uses GOOGLE_APPLICATION_CREDENTIALS env
    collection = db.collection('expenses')
    doc_ref = collection.document()  # auto-ID
    doc_ref.set(record)
    return doc_ref.id
