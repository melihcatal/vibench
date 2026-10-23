import os
from google.cloud import firestore

def store_expense_record(record: dict):
    # Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set for GCP auth
    db = firestore.Client()
    doc_ref = db.collection('expenses').document()
    doc_ref.set(record)
    return doc_ref.id
