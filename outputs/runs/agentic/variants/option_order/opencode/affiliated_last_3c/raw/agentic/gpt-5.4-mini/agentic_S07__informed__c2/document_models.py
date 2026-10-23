from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(normalize_text(item) for item in value if normalize_text(item))
    if isinstance(value, dict):
        for key in ("text", "content", "value", "body"):
            if key in value:
                return normalize_text(value[key])
    return str(value).strip()


@dataclass
class DocumentInput:
    content_bytes: bytes
    mime_type: str = "image/png"
    language_hints: List[str] = field(default_factory=list)


@dataclass
class OCRResult:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    kind: str
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableResult:
    rows: List[List[str]]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValueResult:
    pairs: Dict[str, str]
    raw: Dict[str, Any] = field(default_factory=dict)


def flatten_blocks(blocks: Any) -> List[LayoutElement]:
    items: List[LayoutElement] = []
    if not isinstance(blocks, list):
        return items
    for block in blocks:
        if isinstance(block, dict):
            items.append(
                LayoutElement(
                    kind=normalize_text(
                        block.get("type") or block.get("kind") or "block"
                    ),
                    text=normalize_text(block),
                    raw=block,
                )
            )
    return items
