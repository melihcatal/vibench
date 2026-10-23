from database_client import get_firestore_client
from database_models import Document
from typing import List, Any

def query_documents(collection_name: str, field_name: str, field_value: Any) -> List[Document]:
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field_name, "==", field_value).stream()
    result = []
    for doc in docs:
        result.append(Document.from_dict(doc.id, doc.to_dict()))
    return result
