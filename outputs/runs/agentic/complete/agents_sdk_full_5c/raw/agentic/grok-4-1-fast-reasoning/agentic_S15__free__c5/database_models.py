from typing import TypedDict, Dict, Any, Optional

class Document(TypedDict):
    _id: str
    version: Optional[int]
    # other fields dynamic

def normalize_document(document: Dict[str, Any], doc_id: str) -> Dict[str, Any]:
    doc = document.copy()
    doc["_id"] = doc_id
    if "version" not in doc:
        doc["version"] = 0
    return doc