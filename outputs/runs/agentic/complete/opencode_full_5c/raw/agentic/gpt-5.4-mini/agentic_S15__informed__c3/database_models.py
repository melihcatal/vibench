from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "id" in normalized and "_id" not in normalized:
        normalized["_id"] = normalized["id"]
    return normalized


def normalize_identifier(document: Dict[str, Any]) -> str:
    value = document.get("_id", document.get("id", ""))
    return str(value)


@dataclass
class OperationResult:
    ok: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
