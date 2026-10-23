from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentPage:
    page_number: int
    width: Optional[float] = None
    height: Optional[float] = None
    unit: Optional[str] = None


@dataclass
class TextSpan:
    text: str
    page_number: Optional[int] = None
    confidence: Optional[float] = None
    polygon: List[float] = field(default_factory=list)


@dataclass
class LayoutElement:
    kind: str
    content: str
    page_number: Optional[int] = None
    confidence: Optional[float] = None
    polygon: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    row_span: int = 1
    column_span: int = 1
    page_number: Optional[int] = None
    confidence: Optional[float] = None
    kind: Optional[str] = None


@dataclass
class KeyValueItem:
    key: str
    value: str
    page_number: Optional[int] = None
    confidence: Optional[float] = None


@dataclass
class OCRTextResponse:
    text: str
    pages: List[DocumentPage] = field(default_factory=list)
    spans: List[TextSpan] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-read"


@dataclass
class LayoutResponse:
    elements: List[LayoutElement] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-layout"


@dataclass
class TableResponse:
    tables: List[List[TableCell]] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-layout"


@dataclass
class KeyValueResponse:
    pairs: List[KeyValueItem] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-document"


@dataclass
class NormalizedDocument:
    text: str
    sections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n")).strip()


def chunk_sections(text: str, max_chars: int = 1000) -> List[str]:
    clean = normalize_text(text)
    if not clean:
        return []
    chunks: List[str] = []
    current = ""
    for paragraph in clean.split("\n\n"):
        candidate = paragraph.strip()
        if not candidate:
            continue
        if not current:
            current = candidate
            continue
        if len(current) + 2 + len(candidate) <= max_chars:
            current = current + "\n\n" + candidate
        else:
            chunks.append(current)
            current = candidate
    if current:
        chunks.append(current)
    return chunks
