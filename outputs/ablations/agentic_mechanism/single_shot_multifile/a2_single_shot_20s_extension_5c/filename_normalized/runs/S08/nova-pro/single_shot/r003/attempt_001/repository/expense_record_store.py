import os
from google.cloud import firestore

def store_expense_record(record):
    db = firestore.Client()
    doc_ref = db.collection(u'expenses').document()
    doc_ref.set(record)
    return doc_ref.id