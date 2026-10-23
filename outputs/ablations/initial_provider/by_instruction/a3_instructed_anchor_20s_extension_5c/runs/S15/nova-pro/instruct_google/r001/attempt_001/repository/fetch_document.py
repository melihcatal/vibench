import google.cloud.firestore as firestore

def fetch_document(collection_name, document_id):
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None