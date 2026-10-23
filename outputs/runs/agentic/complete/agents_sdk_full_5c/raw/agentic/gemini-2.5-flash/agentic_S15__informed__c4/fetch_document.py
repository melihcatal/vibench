from database_client import get_firestore_client
from google.cloud.firestore import Client

def fetch_document(collection_name: str, document_id: str):
    """
    Fetches a document by identifier from Google Cloud Firestore.
    """
    db: Client = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"status": "success", "document_id": document_id, "data": doc.to_dict()}
    else:
        return {"status": "not_found", "document_id": document_id}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set up)
    result = fetch_document("users", "user_123")
    print(f"Fetch result: {result}")
