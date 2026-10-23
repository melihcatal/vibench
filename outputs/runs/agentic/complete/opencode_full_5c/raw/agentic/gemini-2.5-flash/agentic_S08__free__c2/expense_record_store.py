from google.cloud import firestore
import os


def persist_expense_record(collection_name: str, record_data: dict) -> str:
    """
    Persists normalized expense records in a Google Cloud Firestore managed document store.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(record_data)
    return doc_ref.id
