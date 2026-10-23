import os
from google.cloud import firestore

def upsert_document(collection_name: str, document_id: str, data: dict):
    """Upserts a JSON document by its primary identifier in Firestore."""
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    return {"status": "success", "document_id": document_id}

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # and Firestore is set up for your project.
    # collection = "my_collection"
    # doc_id = "doc123"
    # document_data = {"name": "Test Document", "value": 123, "active": True}
    # result = upsert_document(collection, doc_id, document_data)
    # print(result)
    pass
