from google.cloud import firestore

db = firestore.client()

def conditional_update(doc_id, updates, condition):
    doc_ref = db.collection(u'documents').document(doc_id)
    doc_ref.update(updates, condition)