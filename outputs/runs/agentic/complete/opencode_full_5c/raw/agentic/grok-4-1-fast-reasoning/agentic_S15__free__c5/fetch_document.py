from typing import Dict, Any, Optional
from database_client import get_documents_collection


def fetch_document(doc_id: str) -> Optional[Dict[str, Any]]:
    collection = get_documents_collection()
    return collection.find_one({"doc_id": doc_id})
