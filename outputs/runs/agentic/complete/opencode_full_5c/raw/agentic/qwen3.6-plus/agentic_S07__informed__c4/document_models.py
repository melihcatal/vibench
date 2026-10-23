from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class BoundingBox:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0


@dataclass
class TextSegment:
    text: str = ""
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None


@dataclass
class LayoutElement:
    element_type: str = ""
    text: str = ""
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None
    children: List["LayoutElement"] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    text: str = ""
    row_index: int = 0
    col_index: int = 0
    row_span: int = 1
    col_span: int = 1
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None
    is_header: bool = False


@dataclass
class TableData:
    cells: List[TableCell] = field(default_factory=list)
    num_rows: int = 0
    num_cols: int = 0
    bounding_box: Optional[BoundingBox] = None
    confidence: float = 0.0


@dataclass
class KeyValue:
    key: str = ""
    value: str = ""
    confidence: float = 0.0
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None


@dataclass
class OcrResult:
    full_text: str = ""
    segments: List[TextSegment] = field(default_factory=list)
    layout_elements: List[LayoutElement] = field(default_factory=list)
    tables: List[TableData] = field(default_factory=list)
    key_values: List[KeyValue] = field(default_factory=list)
    page_count: int = 0
    confidence: float = 0.0


def normalize_bbox(vertex_list) -> BoundingBox:
    if not vertex_list or len(vertex_list) < 4:
        return BoundingBox()
    xs = [v.x for v in vertex_list]
    ys = [v.y for v in vertex_list]
    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)
    return BoundingBox(
        x=min_x,
        y=min_y,
        width=max_x - min_x,
        height=max_y - min_y,
    )


def normalize_text_segment(segment) -> TextSegment:
    text = getattr(segment, "text", "")
    confidence = getattr(segment, "confidence", 0.0)
    bbox = None
    if hasattr(segment, "bounding_poly") and segment.bounding_poly:
        bbox = normalize_bbox(
            segment.bounding_poly.normalized_vertices or segment.bounding_poly.vertices
        )
    return TextSegment(text=text, confidence=confidence, bounding_box=bbox)


def normalize_layout_element(element, element_type="block") -> LayoutElement:
    text = getattr(element, "text_anchor", None)
    text_content = ""
    confidence = 0.0
    if text:
        text_content = getattr(text, "text", "")
        segments = getattr(text, "text_segments", [])
        if segments:
            confidence = sum(getattr(s, "confidence", 0.0) for s in segments) / len(
                segments
            )
    bbox = None
    if hasattr(element, "bounding_poly") and element.bounding_poly:
        bbox = normalize_bbox(
            element.bounding_poly.normalized_vertices or element.bounding_poly.vertices
        )
    return LayoutElement(
        element_type=element_type,
        text=text_content,
        confidence=confidence,
        bounding_box=bbox,
    )


def normalize_table_cell(cell) -> TableCell:
    text = getattr(cell, "text_anchor", None)
    text_content = ""
    confidence = 0.0
    if text:
        text_content = getattr(text, "text", "")
        segments = getattr(text, "text_segments", [])
        if segments:
            confidence = sum(getattr(s, "confidence", 0.0) for s in segments) / len(
                segments
            )
    bbox = None
    if hasattr(cell, "bounding_poly") and cell.bounding_poly:
        bbox = normalize_bbox(
            cell.bounding_poly.normalized_vertices or cell.bounding_poly.vertices
        )
    return TableCell(
        text=text_content,
        row_index=getattr(cell, "row_index", 0),
        col_index=getattr(cell, "col_index", 0),
        row_span=getattr(cell, "row_span", 1),
        col_span=getattr(cell, "col_span", 1),
        confidence=confidence,
        bounding_box=bbox,
        is_header=getattr(cell, "header", False),
    )


def normalize_key_value(pair) -> KeyValue:
    key_text = ""
    value_text = ""
    key_confidence = 0.0
    value_confidence = 0.0
    key_bbox = None
    value_bbox = None

    key_anchor = getattr(pair, "key_text_anchor", None)
    if key_anchor:
        key_text = getattr(key_anchor, "text", "")
        key_segments = getattr(key_anchor, "text_segments", [])
        if key_segments:
            key_confidence = sum(
                getattr(s, "confidence", 0.0) for s in key_segments
            ) / len(key_segments)
        if hasattr(pair, "key_bounding_poly") and pair.key_bounding_poly:
            key_bbox = normalize_bbox(
                pair.key_bounding_poly.normalized_vertices
                or pair.key_bounding_poly.vertices
            )

    value_anchor = getattr(pair, "value_text_anchor", None)
    if value_anchor:
        value_text = getattr(value_anchor, "text", "")
        value_segments = getattr(value_anchor, "text_segments", [])
        if value_segments:
            value_confidence = sum(
                getattr(s, "confidence", 0.0) for s in value_segments
            ) / len(value_segments)
        if hasattr(pair, "value_bounding_poly") and pair.value_bounding_poly:
            value_bbox = normalize_bbox(
                pair.value_bounding_poly.normalized_vertices
                or pair.value_bounding_poly.vertices
            )

    return KeyValue(
        key=key_text,
        value=value_text,
        confidence=(key_confidence + value_confidence) / 2.0
        if (key_confidence or value_confidence)
        else 0.0,
        key_bounding_box=key_bbox,
        value_bounding_box=value_bbox,
    )


def build_ocr_result(document) -> OcrResult:
    full_text = getattr(document, "text", "")
    result = OcrResult(full_text=full_text)

    pages = getattr(document, "pages", [])
    result.page_count = len(pages)

    all_confidences = []
    for page in pages:
        paragraphs = getattr(page, "paragraphs", [])
        for para in paragraphs:
            segments = getattr(getattr(para, "text_anchor", None), "text_segments", [])
            for seg in segments:
                ts = normalize_text_segment(seg)
                result.segments.append(ts)
                if ts.confidence > 0:
                    all_confidences.append(ts.confidence)

        blocks = getattr(page, "blocks", [])
        for block in blocks:
            layout_elem = normalize_layout_element(block, element_type="block")
            result.layout_elements.append(layout_elem)

        tables = getattr(page, "tables", [])
        for table in tables:
            table_cells = getattr(table, "body_rows", [])
            header_rows = getattr(table, "header_rows", [])
            all_rows = (
                header_rows + table_cells
                if hasattr(table, "header_rows")
                else table_cells
            )

            cells = []
            for row_idx, row in enumerate(getattr(table, "header_rows", [])):
                for cell_data in getattr(row, "cells", []):
                    tc = normalize_table_cell(cell_data)
                    tc.row_index = row_idx
                    tc.is_header = True
                    cells.append(tc)
            for row_idx_offset, row in enumerate(getattr(table, "body_rows", [])):
                for cell_data in getattr(row, "cells", []):
                    tc = normalize_table_cell(cell_data)
                    tc.row_index = row_idx_offset + len(
                        getattr(table, "header_rows", [])
                    )
                    cells.append(tc)

            table_bbox = None
            if hasattr(table, "bounding_poly") and table.bounding_poly:
                table_bbox = normalize_bbox(
                    table.bounding_poly.normalized_vertices
                    or table.bounding_poly.vertices
                )

            num_rows = len(getattr(table, "header_rows", [])) + len(
                getattr(table, "body_rows", [])
            )
            num_cols = 0
            if cells:
                num_cols = max(c.col_index + c.col_span for c in cells) if cells else 0

            table_data = TableData(
                cells=cells,
                num_rows=num_rows,
                num_cols=num_cols,
                bounding_box=table_bbox,
                confidence=0.0,
            )
            result.tables.append(table_data)

        form_fields = getattr(page, "form_fields", [])
        for ff in form_fields:
            kv = normalize_key_value(ff)
            result.key_values.append(kv)

    if all_confidences:
        result.confidence = sum(all_confidences) / len(all_confidences)

    return result
