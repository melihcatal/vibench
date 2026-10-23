from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple)):
        return "\n".join(normalize_text(item) for item in value if normalize_text(item))
    return str(value).strip()


def normalize_key_values(items: Any) -> Dict[str, str]:
    result: Dict[str, str] = {}
    if isinstance(items, dict):
        for key, value in items.items():
            result[normalize_text(key)] = normalize_text(value)
        return result
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict):
                key = normalize_text(
                    item.get("key") or item.get("field") or item.get("name")
                )
                value = normalize_text(item.get("value") or item.get("text"))
                if key:
                    result[key] = value
    return result


@dataclass
class DocumentRequest:
    content: bytes
    mime_type: str = "image/jpeg"
    language_hints: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    endpoint: Optional[str] = None
    model: Optional[str] = None


@dataclass
class DocumentResponse:
    text: str = ""
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    lines: List[str] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    key_values: Dict[str, str] = field(default_factory=dict)
    raw: Any = None
