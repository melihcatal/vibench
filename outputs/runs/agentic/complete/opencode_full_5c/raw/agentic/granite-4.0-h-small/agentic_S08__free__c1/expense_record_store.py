# [LATER-STEP] expense_record_store.py

# Persists normalized expense records in an external managed document store (e.g., Firestore)
import os
import json
from google.cloud import firestore
from normalize_expense import NormalizedExpense


def persist_expense(record: NormalizedExpense):
    """Store a normalized expense record in Cloud Firestore."""
    db = firestore.Client()
    collection = db.collection("expenses")
    # Use a deterministic ID or let Firestore auto-generate it
    doc_ref = collection.document()
    doc_ref.set(record.dict())
    return doc_ref.id
