import os
from google.cloud import firestore

db = firestore.client()

def conditional_update(collection_name, document_id, update_data, condition):
    doc_ref = db.collection(collection_name).document(document_id)
    try:
        doc_ref.update(update_data, condition)
        print(f'Document {document_id} updated in collection {collection_name}')
    except Exception as e:
        print(f'Failed to update document {document_id} in collection {collection_name}: {e}')