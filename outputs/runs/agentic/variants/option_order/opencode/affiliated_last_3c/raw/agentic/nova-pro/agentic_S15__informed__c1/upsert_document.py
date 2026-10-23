import os
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()


def upsert_document(doc_id, data):
    doc_ref = db.collection("documents").document(doc_id)
    doc_ref.set(data)
