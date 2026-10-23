import os
from google.cloud import firestore

# Set up the Firestore client
db = firestore.Client()


def message_audit_store(message):
    # Persist processed message records for later lookup
    doc_ref = db.collection("messages").document()
    doc_ref.set(message.to_json())
