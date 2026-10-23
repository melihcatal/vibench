from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "id" in normalized and "_id" not in normalized:
        normalized["_id"] = normalized["id"]
    if "_id" in normalized and "id" not in normalized:
        normalized["id"] = normalized["_id"]
    return normalized


@dataclass
class DocumentWriteResult:
    id: str
    matched: int = 0
    modified: int = 0
    upserted: Optional[bool] = None


@dataclass
class DocumentFetchResult:
    document: Optional[Dict[str, Any]]
