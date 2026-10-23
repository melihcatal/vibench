from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any = None
    confidence: float = 0.0


@dataclass
class DocumentExtractionRequest:
    content: Any
    mime_type: str = "application/pdf"


@dataclass
class DocumentExtractionResponse:
    text: str = ""
    fields: Dict[str, DocumentField] = field(default_factory=dict)
    raw_entities: List[Dict[str, Any]] = field(default_factory=list)


def normalize_confidence(value: Any) -> float:
    try:
        score = float(value)
    except Exception:
        return 0.0
    return max(0.0, min(1.0, score))


def schema_record(fields: Dict[str, Any]) -> Dict[str, Any]:
    return {key: fields.get(key) for key in fields}


def field_map(items: List[Dict[str, Any]]) -> Dict[str, DocumentField]:
    mapped: Dict[str, DocumentField] = {}
    for item in items:
        name = item.get("type") or item.get("name")
        if not name:
            continue
        mapped[name] = DocumentField(
            name=name,
            value=item.get("mention_text") or item.get("value"),
            confidence=normalize_confidence(item.get("confidence", 0.0)),
        )
    return mapped
