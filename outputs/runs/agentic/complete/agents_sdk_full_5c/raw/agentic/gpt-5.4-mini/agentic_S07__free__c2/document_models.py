from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    source_uri: Optional[str] = None
    content_type: str = "application/octet-stream"
    model_id: str = "prebuilt-read"


@dataclass
class OCRResponse:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class LayoutResponse:
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    lines: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class TableResponse:
    tables: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class KeyValueResponse:
    pairs: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class NormalizedDocument:
    text: str
    sections: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_document_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def normalize_key_value_pairs(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in pairs:
        normalized.append({
            "key": str(item.get("key", "")).strip(),
            "value": str(item.get("value", "")).strip(),
            "confidence": float(item.get("confidence", 0.0) or 0.0),
        })
    return normalized
