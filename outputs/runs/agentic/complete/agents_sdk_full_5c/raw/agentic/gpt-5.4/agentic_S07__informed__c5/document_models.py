from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BoundingRegion:
    page_number: int
    polygon: List[float] = field(default_factory=list)


@dataclass
class TextSpan:
    offset: int
    length: int


@dataclass
class LayoutElement:
    kind: str
    content: str = ""
    bounding_regions: List[BoundingRegion] = field(default_factory=list)
    spans: List[TextSpan] = field(default_factory=list)
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCellModel:
    row_index: int
    column_index: int
    content: str
    row_span: int = 1
    column_span: int = 1
    kind: Optional[str] = None
    bounding_regions: List[BoundingRegion] = field(default_factory=list)


@dataclass
class KeyValueModel:
    key: str
    value: str
    confidence: Optional[float] = None
    bounding_regions: List[BoundingRegion] = field(default_factory=list)


@dataclass
class OCRTextResult:
    content: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    model_id: Optional[str] = None


@dataclass
class LayoutResult:
    content: str
    elements: List[LayoutElement] = field(default_factory=list)
    model_id: Optional[str] = None


@dataclass
class TableExtractionResult:
    tables: List[Dict[str, Any]] = field(default_factory=list)
    model_id: Optional[str] = None


@dataclass
class KeyValueExtractionResult:
    pairs: List[KeyValueModel] = field(default_factory=list)
    model_id: Optional[str] = None


@dataclass
class NormalizedDocumentText:
    text: str
    sections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def polygon_to_list(polygon: Any) -> List[float]:
    if not polygon:
        return []
    if isinstance(polygon, list):
        values: List[float] = []
        for point in polygon:
            if isinstance(point, (int, float)):
                values.append(float(point))
            else:
                x = getattr(point, "x", None)
                y = getattr(point, "y", None)
                if x is not None and y is not None:
                    values.extend([float(x), float(y)])
        return values
    return []


def to_bounding_regions(regions: Any) -> List[BoundingRegion]:
    output: List[BoundingRegion] = []
    for region in regions or []:
        output.append(
            BoundingRegion(
                page_number=getattr(region, "page_number", 0) or 0,
                polygon=polygon_to_list(getattr(region, "polygon", None)),
            )
        )
    return output


def normalize_document_text(text: str) -> NormalizedDocumentText:
    cleaned = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    sections = [block.strip() for block in cleaned.split("\n\n") if block.strip()]
    return NormalizedDocumentText(text=cleaned, sections=sections, metadata={"section_count": len(sections)})
