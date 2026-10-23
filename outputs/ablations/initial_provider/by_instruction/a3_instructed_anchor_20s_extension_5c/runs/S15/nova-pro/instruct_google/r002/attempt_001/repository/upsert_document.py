import os
from google.cloud import firestore

db = firestore.client()

def upsert_document(collection_name, document_id, data):
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    print(f'Document {document_id} upserted in collection {collection_name}')