from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BoundingRegion:
    page_number: Optional[int] = None
    polygon: List[float] = field(default_factory=list)

    @classmethod
    def from_azure(cls, region: Any) -> "BoundingRegion":
        return cls(
            page_number=getattr(region, "page_number", None),
            polygon=list(getattr(region, "polygon", []) or []),
        )


@dataclass
class TextLine:
    content: str
    page_number: Optional[int] = None
    polygon: List[float] = field(default_factory=list)


@dataclass
class LayoutBlock:
    kind: str
    content: str
    page_number: Optional[int] = None
    polygon: List[float] = field(default_factory=list)
    confidence: Optional[float] = None


@dataclass
class TableCellModel:
    row_index: int
    column_index: int
    content: str
    kind: Optional[str] = None
    row_span: int = 1
    column_span: int = 1
    page_number: Optional[int] = None


@dataclass
class TableModel:
    row_count: int
    column_count: int
    cells: List[TableCellModel] = field(default_factory=list)


@dataclass
class KeyValueModel:
    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class OCRTextResult:
    text: str
    lines: List[TextLine] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-read"


@dataclass
class LayoutResult:
    blocks: List[LayoutBlock] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-layout"


@dataclass
class TablesResult:
    tables: List[TableModel] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-layout"


@dataclass
class KeyValuesResult:
    pairs: List[KeyValueModel] = field(default_factory=list)
    provider: str = "azure-document-intelligence"
    model_id: str = "prebuilt-document"


def normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def azure_paragraph_kind(paragraph: Any) -> str:
    role = getattr(paragraph, "role", None)
    if role:
        return str(role)
    return "paragraph"


def as_dict(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, "__dict__"):
        return dict(obj.__dict__)
    if isinstance(obj, dict):
        return obj
    return {"value": obj}
