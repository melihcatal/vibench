from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class DocumentInput:
    content: Optional[bytes] = None
    path: Optional[str] = None
    mime_type: str = "application/pdf"


@dataclass
class OCRResult:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Any = None


@dataclass
class LayoutBlock:
    block_type: str
    text: str = ""
    confidence: Optional[float] = None
    raw: Any = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    raw: Any = None


@dataclass
class TableResult:
    cells: List[TableCell] = field(default_factory=list)
    row_count: int = 0
    column_count: int = 0
    raw: Any = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None
    raw: Any = None


@dataclass
class NormalizedDocument:
    text: str
    sections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldExtractionResult:
    fields: Dict[str, str]
    raw: Any = None


@dataclass
class EmbeddingResult:
    vectors: List[List[float]]
    raw: Any = None


def normalize_text(text: str) -> str:
    return "\n".join(line.strip() for line in text.replace("\r\n", "\n").split("\n") if line.strip())


def normalize_blocks(blocks: Iterable[Dict[str, Any]]) -> List[LayoutBlock]:
    normalized: List[LayoutBlock] = []
    for block in blocks:
        normalized.append(
            LayoutBlock(
                block_type=str(block.get("type") or block.get("block_type") or "unknown"),
                text=str(block.get("text") or ""),
                confidence=block.get("confidence"),
                raw=block,
            )
        )
    return normalized


def normalize_key_values(items: Iterable[Dict[str, Any]]) -> List[KeyValuePair]:
    normalized: List[KeyValuePair] = []
    for item in items:
        normalized.append(
            KeyValuePair(
                key=str(item.get("key") or ""),
                value=str(item.get("value") or ""),
                confidence=item.get("confidence"),
                raw=item,
            )
        )
    return normalized
