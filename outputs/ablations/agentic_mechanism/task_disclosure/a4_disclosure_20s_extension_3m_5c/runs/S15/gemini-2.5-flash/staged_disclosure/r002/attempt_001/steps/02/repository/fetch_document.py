from google.cloud import firestore

def fetch_document_from_firestore(collection_name, document_id):
    """Fetches a document by identifier from Google Cloud Firestore."""
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None
