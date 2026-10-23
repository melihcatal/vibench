from typing import Dict, Any
from database_client import get_documents_collection
from database_models import normalize_document


def upsert_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    collection = get_documents_collection()
    normalized = normalize_document(doc)
    collection.replace_one({"doc_id": normalized["doc_id"]}, normalized, upsert=True)
    return normalized
