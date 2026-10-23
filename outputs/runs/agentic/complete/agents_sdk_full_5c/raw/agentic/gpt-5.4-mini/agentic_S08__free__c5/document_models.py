from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    model: str
    schema_name: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentField:
    value: Any
    confidence: float = 0.0


@dataclass
class DocumentResponse:
    raw: Dict[str, Any]
    fields: Dict[str, DocumentField] = field(default_factory=dict)
    model: Optional[str] = None


@dataclass
class NormalizedExpense:
    vendor: str
    date: str
    total: float
    currency: str
    items: List[Dict[str, Any]]
    source: Dict[str, Any] = field(default_factory=dict)


def normalize_text_payload(text: str) -> str:
    return " ".join((text or "").strip().split())


def field_map_from_dict(payload: Dict[str, Any]) -> Dict[str, DocumentField]:
    result: Dict[str, DocumentField] = {}
    for key, value in payload.items():
        if isinstance(value, dict) and "value" in value:
            result[key] = DocumentField(value=value.get("value"), confidence=float(value.get("confidence", 0.0)))
        else:
            result[key] = DocumentField(value=value, confidence=1.0)
    return result
