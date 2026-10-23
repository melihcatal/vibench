import os
from google.cloud import firestore

def upsert_document(collection_name: str, document_id: str, data: dict):
    """Upserts a JSON document by its primary identifier in Firestore."""
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    return {"status": "success", "document_id": document_id}

if __name__ == '__main__':
    # For demonstration, assume GOOGLE_APPLICATION_CREDENTIALS is set
    # and a Firestore project is configured.
    # Replace 'your_collection' and 'your_document_id' with actual values.
    # This is a placeholder for local execution, not part of the core integration logic.
    pass
