from google.cloud import firestore

db = firestore.client()

def fetch_document(doc_id):
    doc_ref = db.collection(u'documents').document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None