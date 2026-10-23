from google.cloud import firestore

db = firestore.client()

def upsert_document(doc_id, data):
    doc_ref = db.collection(u'documents').document(doc_id)
    doc_ref.set(data)