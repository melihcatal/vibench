from typing import Dict, Any, Optional
from google.cloud import firestore
from database_client import get_firestore_client
from database_models import Document

def fetch_document(collection_name: str, document_id: str) -> Optional[Document]:
    """Fetches a document by identifier from a specified Firestore collection.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document to fetch.

    Returns:
        Optional[Document]: A Document object if found, otherwise None.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    try:
        doc = doc_ref.get()
        if doc.exists:
            print(f"Document {document_id} fetched successfully from collection {collection_name}.")
            return Document.from_firestore_document(doc.id, doc.to_dict())
        else:
            print(f"Document {document_id} not found in collection {collection_name}.")
            return None
    except Exception as e:
        print(f"Error fetching document {document_id}: {e}")
        raise

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or running in a GC environment
    # For local testing, ensure Firestore emulator is running or credentials are set up.
    collection = "products"
    existing_doc_id = "product123" # Assuming this document was created by upsert_document.py
    non_existent_doc_id = "nonExistentDoc"

    print(f"Attempting to fetch existing document {existing_doc_id}...")
    try:
        fetched_doc = fetch_document(collection, existing_doc_id)
        if fetched_doc:
            print(f"Fetched Document ID: {fetched_doc.id}")
            print(f"Fetched Document Data: {fetched_doc.data}")

        print(f"\nAttempting to fetch non-existent document {non_existent_doc_id}...")
        not_found_doc = fetch_document(collection, non_existent_doc_id)
        if not_found_doc is None:
            print("As expected, non-existent document was not found.")

    except Exception as e:
        print(f"Example usage failed: {e}")
