from database_client import get_firestore_client
from database_models import Document

def query_documents(collection_name: str, field: str, value: any) -> list[Document]:
    """
    Queries documents by a field value in Google Cloud Firestore.
    """
    db = get_firestore_client()
    
    try:
        docs = db.collection(collection_name).where(field, "==", value).stream()
        results = []
        for doc in docs:
            results.append(Document(doc.id, doc.to_dict()))
        return results
    except Exception as e:
        print(f"Error querying documents: {e}")
        return []

# Provider-identifying signal: google.cloud.firestore
