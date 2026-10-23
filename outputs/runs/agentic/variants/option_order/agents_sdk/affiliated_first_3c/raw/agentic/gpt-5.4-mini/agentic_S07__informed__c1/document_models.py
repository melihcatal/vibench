from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class DocumentInput:
    content: bytes
    content_type: str = "image/png"
    locale: Optional[str] = None
    model: Optional[str] = None
    filename: Optional[str] = None


@dataclass
class TextResult:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Any = None


@dataclass
class LayoutResult:
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    lines: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    raw: Any = None


@dataclass
class TableResult:
    tables: List[Dict[str, Any]] = field(default_factory=list)
    raw: Any = None


@dataclass
class KeyValueResult:
    key_values: List[Dict[str, Any]] = field(default_factory=list)
    raw: Any = None


@dataclass
class TranslationResult:
    translated_text: str
    raw: Any = None


@dataclass
class SafetyResult:
    unsafe: bool
    categories: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class FieldsResult:
    fields: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class EmbeddingResult:
    vectors: List[List[float]] = field(default_factory=list)
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "content", "value", "result"):
            if key in value:
                return normalize_text(value[key])
        return ""
    if isinstance(value, Iterable):
        parts = [normalize_text(v) for v in value]
        return "\n".join(p for p in parts if p)
    return str(value).strip()


def normalize_kv_pairs(pairs: Iterable[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in pairs or []:
        if isinstance(item, dict):
            key = normalize_text(item.get("key") or item.get("name") or item.get("field"))
            value = normalize_text(item.get("value") or item.get("text") or item.get("content"))
            if key or value:
                normalized.append({"key": key, "value": value, "raw": item})
        else:
            normalized.append({"key": "", "value": normalize_text(item), "raw": item})
    return normalized
