from database_client import get_collection
from typing import Dict, Any, Optional


def fetch_document(doc_id: str) -> Optional[Dict[str, Any]]:
    collection = get_collection()
    doc = collection.find_one({"_id": doc_id})
    return dict(doc) if doc else None
