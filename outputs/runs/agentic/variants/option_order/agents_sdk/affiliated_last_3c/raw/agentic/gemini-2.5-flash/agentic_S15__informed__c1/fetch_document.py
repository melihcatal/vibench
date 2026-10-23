from google.cloud import firestore
from database_client import get_firestore_client
from database_models import Document

def fetch_document(collection_name: str, doc_id: str) -> dict | None:
    """Fetches a document by identifier from Firestore."""
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document {doc_id} fetched from collection {collection_name}.")
        return doc.to_dict()
    else:
        print(f"Document {doc_id} not found in collection {collection_name}.")
        return None

if __name__ == '__main__':
    # Example usage (requires Firestore emulator or live project setup)
    # fetched_doc = fetch_document(collection_name="my_collection", doc_id="doc123")
    # if fetched_doc:
    #     print(fetched_doc)
    pass
