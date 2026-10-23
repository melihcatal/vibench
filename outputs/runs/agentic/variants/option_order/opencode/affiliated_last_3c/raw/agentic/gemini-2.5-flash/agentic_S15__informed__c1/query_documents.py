from database_client import get_firestore_client
from typing import List, Dict, Any


def query_documents(
    collection_name: str, field_name: str, field_value: Any
) -> List[Dict[str, Any]]:
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    results = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id  # Include document ID
        results.append(data)
    return results
