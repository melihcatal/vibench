from typing import Any, Dict, Optional, TypedDict
from datetime import datetime


class DocumentRequest(TypedDict):
    id: str
    partition_key: str
    document: Dict[str, Any]
    etag: Optional[str]


class DocumentResponse(TypedDict):
    id: str
    partition_key: str
    document: Dict[str, Any]
    etag: Optional[str]
    last_modified: Optional[datetime]


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = document.copy()
    if "id" not in normalized:
        raise ValueError("Document must contain an 'id' field")
    return normalized
