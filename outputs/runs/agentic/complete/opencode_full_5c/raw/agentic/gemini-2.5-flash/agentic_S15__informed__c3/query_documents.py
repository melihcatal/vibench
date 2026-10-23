from database_client import get_firestore_client
from database_models import Document
from typing import List, Any


def query_documents(collection_name: str, field: str, value: Any) -> List[Document]:
    db = get_firestore_client()
    docs = db.collection(collection_name).where(field, "==", value).stream()
    return [Document(id=doc.id, data=doc.to_dict()) for doc in docs]
