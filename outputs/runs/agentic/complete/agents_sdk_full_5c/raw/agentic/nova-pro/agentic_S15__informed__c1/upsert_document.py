import os
from google.cloud import firestore

db = firestore.client()

def upsert_document(document_id, data):
    doc_ref = db.collection(u'documents').document(document_id)
    doc_ref.set(data)