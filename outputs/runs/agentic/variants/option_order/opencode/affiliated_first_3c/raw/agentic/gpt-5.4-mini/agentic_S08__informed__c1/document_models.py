from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredDocumentRequest:
    document_url: Optional[str] = None
    content_type: str = "application/pdf"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class StructuredDocumentResponse:
    fields: Dict[str, StructuredField]
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_money(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {"amount": value, "currency": None}


def normalize_expense_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": payload.get("vendor"),
        "date": payload.get("date"),
        "total": normalize_money(payload.get("total")),
        "line_items": payload.get("line_items", []),
        "merchant": payload.get("merchant"),
        "tax": normalize_money(payload.get("tax")),
        "items": payload.get("items", []),
    }
