import os
from google.cloud import firestore


def expense_record_store(expense):
    db = firestore.Client(credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    doc_ref = db.collection("expenses").document()
    doc_ref.set(expense)
