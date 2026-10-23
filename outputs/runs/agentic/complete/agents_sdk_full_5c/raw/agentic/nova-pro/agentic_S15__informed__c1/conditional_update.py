import os
from google.cloud import firestore

db = firestore.client()

def conditional_update(document_id, data, condition):
    doc_ref = db.collection(u'documents').document(document_id)
    doc_ref.update(data, condition)