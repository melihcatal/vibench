from database_client import get_firestore_client
from google.cloud.firestore import Client

def upsert_document(collection_name: str, document_id: str, data: dict):
    """
    Upserts a JSON document into Google Cloud Firestore by its primary identifier.
    """
    db: Client = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    return {"status": "success", "document_id": document_id}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set up)
    sample_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "city": "New York",
        "is_active": True
    }
    result = upsert_document("users", "user_123", sample_data)
    print(f"Upsert result: {result}")
