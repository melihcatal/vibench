from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class DocumentRequest:
    file_path: Optional[str] = None
    file_bytes: Optional[bytes] = None
    mime_type: Optional[str] = None
    language_hint: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload = asdict(self)
        if self.file_bytes is not None:
            payload["file_bytes"] = self.file_bytes
        return payload


@dataclass
class TextResult:
    text: str
    pages: List[str] = field(default_factory=list)
    raw: Any = None


@dataclass
class LayoutBlock:
    kind: str
    text: str
    bounding_box: Optional[List[float]] = None
    confidence: Optional[float] = None
    raw: Any = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    raw: Any = None


@dataclass
class TableResult:
    cells: List[TableCell] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    raw: Any = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None
    raw: Any = None


@dataclass
class ExtractionResponse:
    items: List[Any] = field(default_factory=list)
    text: str = ""
    raw: Any = None


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Any = None


@dataclass
class SafetyResult:
    text: str
    unsafe: bool
    categories: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None


@dataclass
class FieldExtractionResult:
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
    if isinstance(value, Mapping):
        for key in ("text", "content", "value", "ocr_text"):
            if key in value:
                return normalize_text(value[key])
        return " ".join(normalize_text(v) for v in value.values()).strip()
    if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray)):
        return "\n".join(normalize_text(v) for v in value if normalize_text(v))
    return str(value).strip()


def normalize_key_value_pairs(items: Iterable[Mapping[str, Any]]) -> List[KeyValuePair]:
    normalized: List[KeyValuePair] = []
    for item in items:
        normalized.append(
            KeyValuePair(
                key=normalize_text(item.get("key") or item.get("name") or item.get("field")),
                value=normalize_text(item.get("value") or item.get("text") or item.get("content")),
                confidence=item.get("confidence"),
                raw=dict(item),
            )
        )
    return normalized
