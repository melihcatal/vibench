import os
from google.cloud import firestore


def message_audit_store(message):
    db = firestore.Client()
    doc_ref = db.collection("messages").document()
    doc_ref.set(message)
