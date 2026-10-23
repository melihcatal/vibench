from typing import List, Dict, Any
from database_client import get_firestore_client
from database_models import Document

def query_documents(collection_name: str, field_name: str, field_value: Any) -> List[Document]:
    """
    Queries documents by a field value from Google Firestore.
    """
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    
    results = []
    for doc in docs:
        results.append(Document.from_dict(doc.id, doc.to_dict()))
    return results

if __name__ == "__main__":
    # Example usage
    # Assuming 'my_collection' has documents with a 'value' field
    query_results = query_documents("my_collection", "value", 100)
    for doc in query_results:
        print(f"Queried document: {doc.id} -> {doc.data}")
