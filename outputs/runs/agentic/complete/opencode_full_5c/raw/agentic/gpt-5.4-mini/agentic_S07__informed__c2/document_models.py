from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _normalize_whitespace(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def normalize_text(value: Any) -> str:
    return _normalize_whitespace(value)


def normalize_blocks(items: Any) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items or []:
        if isinstance(item, dict):
            normalized.append({k: item[k] for k in item})
        else:
            normalized.append({"text": normalize_text(item)})
    return normalized


@dataclass
class DocumentInput:
    source: str
    mime_type: str = "image/jpeg"
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OCRResponse:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutResponse:
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableResponse:
    tables: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValueResponse:
    pairs: Dict[str, str] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)
