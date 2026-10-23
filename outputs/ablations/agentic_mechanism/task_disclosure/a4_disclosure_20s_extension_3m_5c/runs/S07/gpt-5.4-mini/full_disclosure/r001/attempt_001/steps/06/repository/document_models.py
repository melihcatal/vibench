from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class DocumentProcessingError(ValueError):
    pass


class ExtractionKind(str, Enum):
    OCR = "ocr"
    LAYOUT = "layout"


@dataclass(frozen=True)
class DocumentInput:
    content: bytes
    filename: Optional[str] = None
    content_type: Optional[str] = None


@dataclass(frozen=True)
class OCRRequest:
    document: DocumentInput
    language: Optional[str] = None
    include_confidence: bool = True


@dataclass(frozen=True)
class LayoutRequest:
    document: DocumentInput
    detect_tables: bool = True
    detect_blocks: bool = True
    detect_lines: bool = True


@dataclass(frozen=True)
class NormalizedSpan:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    confidence: Optional[float] = None


@dataclass(frozen=True)
class BoundingBox:
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height


@dataclass(frozen=True)
class OCRLine:
    text: str
    spans: Tuple[NormalizedSpan, ...] = ()
    confidence: Optional[float] = None
    bbox: Optional[BoundingBox] = None


@dataclass(frozen=True)
class OCRPage:
    page_number: int
    text: str
    lines: Tuple[OCRLine, ...] = ()
    confidence: Optional[float] = None


@dataclass(frozen=True)
class OCRResponse:
    text: str
    pages: Tuple[OCRPage, ...] = ()
    language: Optional[str] = None
    confidence: Optional[float] = None
    raw: Any = None


@dataclass(frozen=True)
class LayoutBlock:
    block_type: str
    text: str = ""
    bbox: Optional[BoundingBox] = None
    confidence: Optional[float] = None
    page_number: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LayoutTableCell:
    row_index: int
    column_index: int
    text: str
    bbox: Optional[BoundingBox] = None
    confidence: Optional[float] = None


@dataclass(frozen=True)
class LayoutTableRow:
    row_index: int
    cells: Tuple[LayoutTableCell, ...]


@dataclass(frozen=True)
class LayoutTable:
    rows: Tuple[LayoutTableRow, ...]
    bbox: Optional[BoundingBox] = None
    confidence: Optional[float] = None


@dataclass(frozen=True)
class LayoutResponse:
    blocks: Tuple[LayoutBlock, ...] = ()
    tables: Tuple[LayoutTable, ...] = ()
    raw: Any = None


def normalize_whitespace(text: Optional[str]) -> str:
    if not text:
        return ""
    return " ".join(text.replace("\u00a0", " ").split())


def normalize_ocr_text(text: Optional[str]) -> str:
    return normalize_whitespace(text)


def normalize_layout_text(text: Optional[str]) -> str:
    return normalize_whitespace(text)


def normalize_ocr_response(response: Any) -> OCRResponse:
    if isinstance(response, OCRResponse):
        return response
    if not isinstance(response, dict):
        raise DocumentProcessingError("OCR response must be a dict or OCRResponse")
    pages_data = response.get("pages") or []
    pages: List[OCRPage] = []
    for page in pages_data:
        lines: List[OCRLine] = []
        for line in page.get("lines", []) or []:
            spans = tuple(
                NormalizedSpan(
                    text=normalize_ocr_text(span.get("text")),
                    start=span.get("start"),
                    end=span.get("end"),
                    confidence=span.get("confidence"),
                )
                for span in line.get("spans", []) or []
            )
            bbox = line.get("bbox")
            lines.append(
                OCRLine(
                    text=normalize_ocr_text(line.get("text")),
                    spans=spans,
                    confidence=line.get("confidence"),
                    bbox=BoundingBox(**bbox) if isinstance(bbox, dict) else None,
                )
            )
        pages.append(
            OCRPage(
                page_number=int(page.get("page_number", 0)),
                text=normalize_ocr_text(page.get("text")),
                lines=tuple(lines),
                confidence=page.get("confidence"),
            )
        )
    return OCRResponse(
        text=normalize_ocr_text(response.get("text")),
        pages=tuple(pages),
        language=response.get("language"),
        confidence=response.get("confidence"),
        raw=response,
    )


def normalize_layout_response(response: Any) -> LayoutResponse:
    if isinstance(response, LayoutResponse):
        return response
    if not isinstance(response, dict):
        raise DocumentProcessingError("Layout response must be a dict or LayoutResponse")
    blocks: List[LayoutBlock] = []
    for block in response.get("blocks", []) or []:
        bbox = block.get("bbox")
        blocks.append(
            LayoutBlock(
                block_type=str(block.get("block_type", block.get("type", "unknown"))),
                text=normalize_layout_text(block.get("text")),
                bbox=BoundingBox(**bbox) if isinstance(bbox, dict) else None,
                confidence=block.get("confidence"),
                page_number=block.get("page_number"),
                metadata=dict(block.get("metadata") or {}),
            )
        )
    tables: List[LayoutTable] = []
    for table in response.get("tables", []) or []:
        rows: List[LayoutTableRow] = []
        for row in table.get("rows", []) or []:
            cells: List[LayoutTableCell] = []
            for cell in row.get("cells", []) or []:
                bbox = cell.get("bbox")
                cells.append(
                    LayoutTableCell(
                        row_index=int(cell.get("row_index", row.get("row_index", 0))),
                        column_index=int(cell.get("column_index", 0)),
                        text=normalize_layout_text(cell.get("text")),
                        bbox=BoundingBox(**bbox) if isinstance(bbox, dict) else None,
                        confidence=cell.get("confidence"),
                    )
                )
            rows.append(LayoutTableRow(row_index=int(row.get("row_index", 0)), cells=tuple(cells)))
        bbox = table.get("bbox")
        tables.append(
            LayoutTable(
                rows=tuple(rows),
                bbox=BoundingBox(**bbox) if isinstance(bbox, dict) else None,
                confidence=table.get("confidence"),
            )
        )
    return LayoutResponse(blocks=tuple(blocks), tables=tuple(tables), raw=response)


def build_ocr_request(content: bytes, filename: Optional[str] = None, content_type: Optional[str] = None, language: Optional[str] = None, include_confidence: bool = True) -> OCRRequest:
    return OCRRequest(document=DocumentInput(content=content, filename=filename, content_type=content_type), language=language, include_confidence=include_confidence)


def build_layout_request(content: bytes, filename: Optional[str] = None, content_type: Optional[str] = None, detect_tables: bool = True, detect_blocks: bool = True, detect_lines: bool = True) -> LayoutRequest:
    return LayoutRequest(document=DocumentInput(content=content, filename=filename, content_type=content_type), detect_tables=detect_tables, detect_blocks=detect_blocks, detect_lines=detect_lines)
