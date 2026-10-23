from database_client import get_firestore_client, get_collection_name
from database_models import Document
from typing import List, Dict, Any


def query_documents(field_name: str, field_value: Any) -> List[Document]:
    """
    Queries documents by a field value or partition-style key in Google Firestore.
    """
    db = get_firestore_client()
    collection_name = get_collection_name()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    result = []
    for doc in docs:
        result.append(Document(id=doc.id, data=doc.to_dict()))
    return result
