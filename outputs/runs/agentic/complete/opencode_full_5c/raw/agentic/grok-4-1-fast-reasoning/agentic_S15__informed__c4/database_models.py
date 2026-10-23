from typing import Any, Dict, List, Optional

Document = Dict[str, Any]


def normalize_document(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if doc is None:
        return None
    normalized = dict(doc)
    if "_id" in normalized:
        normalized["id"] = str(normalized["_id"])
        del normalized["_id"]
    return normalized


def normalize_documents(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_document(doc) for doc in docs]
