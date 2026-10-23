from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_bytes: bytes
    mime_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentResponse:
    fields: Dict[str, Any]
    items: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Any] = None


def normalize_items(items):
    normalized = []
    for item in items or []:
        normalized.append({
            "description": item.get("description"),
            "quantity": item.get("quantity"),
            "amount": item.get("amount"),
        })
    return normalized


def normalize_response(fields=None, items=None, raw=None):
    return DocumentResponse(fields=fields or {}, items=normalize_items(items), raw=raw)
