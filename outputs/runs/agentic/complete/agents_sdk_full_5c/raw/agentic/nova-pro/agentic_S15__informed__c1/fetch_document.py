import os
from google.cloud import firestore

db = firestore.client()

def fetch_document(document_id):
    doc_ref = db.collection(u'documents').document(document_id)
    doc = doc_ref.get()
    return doc.to_dict()