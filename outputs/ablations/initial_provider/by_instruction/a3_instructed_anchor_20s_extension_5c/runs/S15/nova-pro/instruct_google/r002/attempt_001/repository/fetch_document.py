import os
from google.cloud import firestore

db = firestore.client()

def fetch_document(collection_name, document_id):
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document {document_id} fetched from collection {collection_name}')
        return doc.to_dict()
    else:
        print(f'Document {document_id} not found in collection {collection_name}')
        return None