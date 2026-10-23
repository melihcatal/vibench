from database_client import get_firestore_client

def upsert_document(collection_name: str, document_id: str, data: dict):
    """Upserts a JSON document into Firestore by its primary identifier."""
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    print(f"Document {document_id} upserted in collection {collection_name}.")

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    sample_data = {
        "name": "Alice",
        "age": 30,
        "city": "New York"
    }
    upsert_document("users", "user123", sample_data)
