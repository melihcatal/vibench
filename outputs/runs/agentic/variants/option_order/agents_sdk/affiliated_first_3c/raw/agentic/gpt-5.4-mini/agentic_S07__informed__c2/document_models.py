from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentInput:
    source_url: Optional[str] = None
    file_path: Optional[str] = None
    language: Optional[str] = None


@dataclass
class TextExtractionResult:
    text: str
    pages: List[int] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-read"


@dataclass
class LayoutElement:
    kind: str
    content: str
    page_number: Optional[int] = None
    bounding_regions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class LayoutExtractionResult:
    elements: List[LayoutElement] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-layout"


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    row_span: int = 1
    column_span: int = 1


@dataclass
class TableExtractionResult:
    tables: List[List[TableCell]] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-layout"


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class KeyValueExtractionResult:
    pairs: List[KeyValuePair] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-document"


@dataclass
class NormalizedDocumentText:
    text: str
    sections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> NormalizedDocumentText:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return NormalizedDocumentText(text="\n".join(lines), sections=lines, metadata={"line_count": len(lines)})
