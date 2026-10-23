import os
from google.cloud import firestore


def persist_audit_record(record):
    db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc = db.collection("federated_login_audit").document()
    doc.set(record)
    return doc.id
