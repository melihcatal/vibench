import google.cloud.firestore as firestore

def upsert_document(collection_name, document_id, document_data):
    db = firestore.Client()
    collection_ref = db.collection(collection_name)
    doc_ref = collection_ref.document(document_id)
    doc_ref.set(document_data)