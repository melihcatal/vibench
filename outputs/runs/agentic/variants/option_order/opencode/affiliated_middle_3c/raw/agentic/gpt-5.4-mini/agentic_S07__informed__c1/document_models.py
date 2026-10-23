from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    source: str
    content_type: Optional[str] = None


@dataclass
class DocumentResponse:
    raw: Any
    text: str = ''
    layout: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    key_values: List[Dict[str, Any]] = field(default_factory=list)


def normalize_response_text(raw: Any) -> str:
    if raw is None:
        return ''
    if isinstance(raw, str):
        return raw.strip()
    if hasattr(raw, 'content') and isinstance(raw.content, str):
        return raw.content.strip()
    return str(raw).strip()


def normalize_layout_items(items: Any) -> List[Dict[str, Any]]:
    if not items:
        return []
    normalized = []
    for item in items:
        normalized.append({k: v for k, v in getattr(item, '__dict__', {}).items() if not k.startswith('_')})
    return normalized
