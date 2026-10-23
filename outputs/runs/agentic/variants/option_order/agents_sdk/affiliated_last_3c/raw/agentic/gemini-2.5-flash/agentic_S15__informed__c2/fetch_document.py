import os
from google.cloud import firestore

def fetch_document(collection_name: str, document_id: str):
    """Fetches a document by identifier from Firestore."""
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"status": "success", "document": doc.to_dict()}
    else:
        return {"status": "not_found", "document_id": document_id}

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # and Firestore is set up for your project.
    # collection = "my_collection"
    # doc_id = "doc123"
    # result = fetch_document(collection, doc_id)
    # print(result)
    pass
