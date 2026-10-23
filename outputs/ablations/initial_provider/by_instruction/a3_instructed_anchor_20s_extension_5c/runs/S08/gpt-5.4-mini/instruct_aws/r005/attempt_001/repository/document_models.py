from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class DocumentExtractionRequest:
    document_bytes: bytes
    content_type: str = "application/pdf"
    scenario: str = "invoice"


@dataclass
class DocumentExtractionResponse:
    provider: str
    fields: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


def build_normalized_expense(fields: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "merchant": fields.get("merchant") or fields.get("vendor"),
        "date": fields.get("date"),
        "total": fields.get("total"),
        "tax": fields.get("tax"),
        "items": fields.get("items", []),
        "line_items": fields.get("line_items", []),
        "notes": fields.get("notes", ""),
    }


def ensure_required_fields(payload: Dict[str, Any], required: List[str]) -> List[str]:
    return [name for name in required if payload.get(name) in (None, "", [])]
