import os
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()


def conditional_update(doc_id, update_data, condition):
    doc_ref = db.collection("documents").document(doc_id)
    doc_ref.update(update_data, condition)
