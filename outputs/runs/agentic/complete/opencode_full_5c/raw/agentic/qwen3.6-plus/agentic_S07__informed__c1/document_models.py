from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class OCRRequest:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    content_type: str = "application/octet-stream"
    locale: Optional[str] = None


@dataclass
class OCRTextResponse:
    text: str = ""
    confidence: float = 0.0
    page_count: int = 0
    raw_result: Optional[Any] = None


@dataclass
class LayoutBlock:
    block_type: str
    content: str
    bounding_regions: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class OCRLayoutResponse:
    blocks: List[LayoutBlock] = field(default_factory=list)
    page_count: int = 0
    raw_result: Optional[Any] = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    row_span: int = 1
    column_span: int = 1
    bounding_regions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TableData:
    row_count: int
    column_count: int
    cells: List[TableCell] = field(default_factory=list)
    bounding_regions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OCRTableResponse:
    tables: List[TableData] = field(default_factory=list)
    page_count: int = 0
    raw_result: Optional[Any] = None


@dataclass
class KeyValue:
    key: str
    value: str
    confidence: float = 0.0


@dataclass
class OCRKeyValueResponse:
    key_values: List[KeyValue] = field(default_factory=list)
    page_count: int = 0
    raw_result: Optional[Any] = None


def normalize_text_response(raw_result) -> OCRTextResponse:
    content = raw_result.content if hasattr(raw_result, "content") else ""
    confidence = 0.0
    if hasattr(raw_result, "pages") and raw_result.pages:
        confidences = []
        for page in raw_result.pages:
            if hasattr(page, "spans") and page.spans:
                confidences.append(1.0)
        if confidences:
            confidence = sum(confidences) / len(confidences)
    page_count = (
        len(raw_result.pages)
        if hasattr(raw_result, "pages") and raw_result.pages
        else 0
    )
    return OCRTextResponse(
        text=content.strip(),
        confidence=confidence,
        page_count=page_count,
        raw_result=raw_result,
    )


def normalize_layout_response(raw_result) -> OCRLayoutResponse:
    blocks = []
    if hasattr(raw_result, "paragraphs") and raw_result.paragraphs:
        for para in raw_result.paragraphs:
            regions = []
            if para.bounding_regions:
                for r in para.bounding_regions:
                    regions.append({"page_number": r.page_number, "polygon": r.polygon})
            blocks.append(
                LayoutBlock(
                    block_type="paragraph",
                    content=para.content,
                    bounding_regions=regions,
                    confidence=getattr(para, "confidence", 0.0),
                )
            )
    if hasattr(raw_result, "tables") and raw_result.tables:
        for table in raw_result.tables:
            regions = []
            if table.bounding_regions:
                for r in table.bounding_regions:
                    regions.append({"page_number": r.page_number, "polygon": r.polygon})
            blocks.append(
                LayoutBlock(
                    block_type="table",
                    content=f"Table ({table.row_count}x{table.column_count})",
                    bounding_regions=regions,
                    confidence=getattr(table, "confidence", 0.0),
                )
            )
    page_count = (
        len(raw_result.pages)
        if hasattr(raw_result, "pages") and raw_result.pages
        else 0
    )
    return OCRLayoutResponse(
        blocks=blocks, page_count=page_count, raw_result=raw_result
    )


def normalize_table_response(raw_result) -> OCRTableResponse:
    tables = []
    if hasattr(raw_result, "tables") and raw_result.tables:
        for table in raw_result.tables:
            cells = []
            if table.cells:
                for cell in table.cells:
                    regions = []
                    if cell.bounding_regions:
                        for r in cell.bounding_regions:
                            regions.append(
                                {"page_number": r.page_number, "polygon": r.polygon}
                            )
                    cells.append(
                        TableCell(
                            row_index=cell.row_index,
                            column_index=cell.column_index,
                            content=cell.content,
                            row_span=cell.row_span,
                            column_span=cell.column_span,
                            bounding_regions=regions,
                        )
                    )
            regions = []
            if table.bounding_regions:
                for r in table.bounding_regions:
                    regions.append({"page_number": r.page_number, "polygon": r.polygon})
            tables.append(
                TableData(
                    row_count=table.row_count,
                    column_count=table.column_count,
                    cells=cells,
                    bounding_regions=regions,
                )
            )
    page_count = (
        len(raw_result.pages)
        if hasattr(raw_result, "pages") and raw_result.pages
        else 0
    )
    return OCRTableResponse(tables=tables, page_count=page_count, raw_result=raw_result)


def normalize_kv_response(raw_result) -> OCRKeyValueResponse:
    key_values = []
    if hasattr(raw_result, "key_value_pairs") and raw_result.key_value_pairs:
        for kv in raw_result.key_value_pairs:
            key_content = kv.key.content if kv.key else ""
            value_content = kv.value.content if kv.value else ""
            key_values.append(
                KeyValue(
                    key=key_content,
                    value=value_content,
                    confidence=kv.confidence,
                )
            )
    page_count = (
        len(raw_result.pages)
        if hasattr(raw_result, "pages") and raw_result.pages
        else 0
    )
    return OCRKeyValueResponse(
        key_values=key_values, page_count=page_count, raw_result=raw_result
    )
