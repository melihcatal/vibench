from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredDocumentRequest:
    document_text: str
    document_type: str
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredDocumentField:
    value: Any
    confidence: float = 0.0
    source: Optional[str] = None


@dataclass
class StructuredDocumentResponse:
    fields: Dict[str, StructuredDocumentField] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


def field_payload(value: Any, confidence: float = 0.0, source: Optional[str] = None) -> Dict[str, Any]:
    payload = {"value": value, "confidence": confidence}
    if source is not None:
        payload["source"] = source
    return payload


def normalize_line_items(items: Any) -> List[Dict[str, Any]]:
    normalized = []
    if not items:
        return normalized
    for item in items:
        if isinstance(item, dict):
            normalized.append({
                "description": item.get("description") or item.get("name") or "",
                "quantity": item.get("quantity", 1),
                "unit_price": item.get("unit_price", item.get("price")),
                "amount": item.get("amount", item.get("total")),
                "confidence": item.get("confidence", 0.0),
            })
    return normalized
