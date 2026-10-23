from database_client import get_firestore_client
from google.cloud.firestore import Client
from typing import List, Dict, Any

def query_documents(collection_name: str, field: str, value: Any) -> List[Dict[str, Any]]:
    """
    Queries documents by a field value in Google Cloud Firestore.
    """
    db: Client = get_firestore_client()
    docs = (
        db.collection(collection_name).where(field, "==", value).stream()
    )
    results = []
    for doc in docs:
        results.append({"document_id": doc.id, "data": doc.to_dict()})
    return {"status": "success", "results": results}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set up)
    # Assuming some documents with 'city' field exist
    result = query_documents("users", "city", "New York")
    print(f"Query result: {result}")
