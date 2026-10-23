import os
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()


def fetch_document(doc_id):
    doc_ref = db.collection("documents").document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
