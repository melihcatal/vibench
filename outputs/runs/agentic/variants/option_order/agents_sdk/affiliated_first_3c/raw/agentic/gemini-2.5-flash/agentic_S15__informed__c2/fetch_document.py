from database_client import get_firestore_client

def fetch_document(collection_name: str, document_id: str) -> dict | None:
    """Fetches a document by identifier from Firestore."""
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
        return doc.to_dict()
    else:
        print(f"Document {document_id} not found in collection {collection_name}.")
        return None

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    fetched_doc = fetch_document("users", "user123")
    if fetched_doc:
        print(f"Successfully fetched: {fetched_doc}")
