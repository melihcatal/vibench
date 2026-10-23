from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return text.strip()
    return str(text).strip()


def normalize_items(items: Any) -> List[Dict[str, Any]]:
    if not items:
        return []
    if isinstance(items, list):
        return [item if isinstance(item, dict) else {"value": item} for item in items]
    return [{"value": items}]


@dataclass
class DocumentRequest:
    document_bytes: bytes
    region: Optional[str] = None
    language: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class DocumentResponse:
    text: str = ""
    blocks: Optional[List[Dict[str, Any]]] = None
    tables: Optional[List[Dict[str, Any]]] = None
    key_values: Optional[Dict[str, str]] = None
