from typing import Dict, Any
from datetime import datetime


def normalize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    doc = doc.copy()
    if "doc_id" not in doc:
        raise ValueError("doc_id required")
    if "version" not in doc:
        doc["version"] = 0
    if "created_at" not in doc:
        doc["created_at"] = datetime.utcnow().isoformat()
    doc["updated_at"] = datetime.utcnow().isoformat()
    return doc
