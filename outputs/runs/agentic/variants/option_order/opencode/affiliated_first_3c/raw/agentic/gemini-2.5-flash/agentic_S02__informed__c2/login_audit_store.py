import os
import datetime
from google.cloud import firestore


def store_audit_record(record: dict):
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    db = firestore.Client()
    doc_ref = db.collection("login_audit_records").document()

    record["timestamp"] = firestore.SERVER_TIMESTAMP

    doc_ref.set(record)
    return doc_ref.id
