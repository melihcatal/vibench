from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentSource:
    path: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None


@dataclass
class StructuredDocumentRequest:
    document: DocumentSource
    schema_name: str
    schema: Dict[str, Any]
    provider: str = "openai"
    model: str = "gpt-4.1-mini"


@dataclass
class StructuredDocumentResponse:
    provider: str
    model: str
    content: Dict[str, Any]
    raw: Optional[Dict[str, Any]] = None


def normalize_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except Exception:
        confidence = 0.0
    if confidence < 0.0:
        return 0.0
    if confidence > 1.0:
        return 1.0
    return confidence


def standardize_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(item)
    return normalized
