"""
document_models.py - Request, response, and normalization helpers
for Azure AI Document Intelligence OCR and Layout Extraction.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TextBlock:
    """Normalized text block with bounding box."""
    content: str
    confidence: float
    bounding_box: Optional[List[float]] = field(default_factory=list)
    page_number: int = 0


@dataclass
class LayoutBlock:
    """Normalized layout element."""
    block_type: str  # paragraph, heading, table, figure, list-item, etc.
    content: str
    confidence: float
    bounding_box: Optional[List[float]] = field(default_factory=list)
    page_number: int = 0


@dataclass
class TableCell:
    """Normalized table cell."""
    row_index: int
    column_index: int
    content: str
    confidence: float
    row_span: int = 1
    column_span: int = 1


@dataclass
class TableRow:
    """Normalized table row."""
    row_index: int
    cells: List[TableCell]


@dataclass
class Table:
    """Normalized table structure."""
    row_count: int
    column_count: int
    rows: List[TableRow]


@dataclass
class KeyValue:
    """Normalized key-value pair from a form."""
    key: str
    value: str
    confidence: float
    bounding_box: Optional[List[float]] = field(default_factory=list)


@dataclass
class OcrResponse:
    """Normalized OCR response."""
    text: str = ""
    blocks: List[TextBlock] = field(default_factory=list)
    page_count: int = 0


@dataclass
class LayoutResponse:
    """Normalized layout response."""
    blocks: List[LayoutBlock] = field(default_factory=list)
    tables: List[Table] = field(default_factory=list)
    page_count: int = 0


@dataclass
class TableResponse:
    """Normalized table extraction response."""
    tables: List[Table] = field(default_factory=list)
    page_count: int = 0


@dataclass
class KeyValueResponse:
    """Normalized key-value extraction response."""
    pairs: List[KeyValue] = field(default_factory=list)
    page_count: int = 0


def normalize_azure_text_result(result) -> OcrResponse:
    """Normalize Azure Document Intelligence OCR result to OcrResponse."""
    blocks = []
    all_text = []
    if result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    content = line.content or ""
                    all_text.append(content)
                    bbox = []
                    if hasattr(line, 'bounding_regions') and line.bounding_regions:
                        bbox = [
                            coord
                            for region in line.bounding_regions
                            for coord in [
                                region.polygon[0].x, region.polygon[0].y,
                                region.polygon[2].x, region.polygon[2].y,
                            ]
                        ]
                    blocks.append(TextBlock(
                        content=content,
                        confidence=getattr(line, 'confidence', 0.0),
                        bounding_box=bbox,
                        page_number=getattr(page, 'page_number', 0),
                    ))
    return OcrResponse(
        text="\n".join(all_text),
        blocks=blocks,
        page_count=len(result.pages) if result.pages else 0,
    )


def normalize_azure_layout_result(result) -> LayoutResponse:
    """Normalize Azure Document Intelligence layout result to LayoutResponse."""
    layout_blocks = []
    tables = []
    if result.pages:
        for page in result.pages:
            if hasattr(page, 'paragraphs') and page.paragraphs:
                for para in page.paragraphs:
                    role = getattr(para, 'role', '') or 'paragraph'
                    layout_blocks.append(LayoutBlock(
                        block_type=role,
                        content=para.content or "",
                        confidence=getattr(para, 'confidence', 0.0),
                        page_number=getattr(page, 'page_number', 0),
                    ))
            if hasattr(page, 'tables') and page.tables:
                for azure_table in page.tables:
                    cells = []
                    if hasattr(azure_table, 'cells'):
                        for cell in azure_table.cells:
                            cells.append(TableCell(
                                row_index=getattr(cell, 'row_index', 0),
                                column_index=getattr(cell, 'column_index', 0),
                                content=cell.content or "",
                                confidence=getattr(cell, 'confidence', 0.0),
                                row_span=getattr(cell, 'row_span', 1),
                                column_span=getattr(cell, 'column_span', 1),
                            ))
                    row_groups = {}
                    for c in cells:
                        row_groups.setdefault(c.row_index, []).append(c)
                    rows = [
                        TableRow(row_index=ri, cells=row_cells)
                        for ri, row_cells in sorted(row_groups.items())
                    ]
                    tables.append(Table(
                        row_count=getattr(azure_table, 'row_count', len(rows)),
                        column_count=getattr(azure_table, 'column_count', 0),
                        rows=rows,
                    ))
    return LayoutResponse(
        blocks=layout_blocks,
        tables=tables,
        page_count=len(result.pages) if result.pages else 0,
    )


def normalize_azure_table_result(result) -> TableResponse:
    """Normalize Azure table extraction to TableResponse."""
    tables = []
    if result.pages:
        for page in result.pages:
            if hasattr(page, 'tables') and page.tables:
                for azure_table in page.tables:
                    cells = []
                    if hasattr(azure_table, 'cells'):
                        for cell in azure_table.cells:
                            cells.append(TableCell(
                                row_index=getattr(cell, 'row_index', 0),
                                column_index=getattr(cell, 'column_index', 0),
                                content=cell.content or "",
                                confidence=getattr(cell, 'confidence', 0.0),
                                row_span=getattr(cell, 'row_span', 1),
                                column_span=getattr(cell, 'column_span', 1),
                            ))
                    row_groups = {}
                    for c in cells:
                        row_groups.setdefault(c.row_index, []).append(c)
                    rows = [
                        TableRow(row_index=ri, cells=row_cells)
                        for ri, row_cells in sorted(row_groups.items())
                    ]
                    tables.append(Table(
                        row_count=getattr(azure_table, 'row_count', len(rows)),
                        column_count=getattr(azure_table, 'column_count', 0),
                        rows=rows,
                    ))
    return TableResponse(
        tables=tables,
        page_count=len(result.pages) if result.pages else 0,
    )


def normalize_azure_keyvalue_result(result) -> KeyValueResponse:
    """Normalize Azure key-value pair extraction to KeyValueResponse."""
    pairs = []
    if hasattr(result, 'documents') and result.documents:
        for doc in result.documents:
            if hasattr(doc, 'fields') and doc.fields:
                for field_name, field_value in doc.fields.items():
                    value_str = ""
                    if hasattr(field_value, 'value'):
                        value_str = str(field_value.value) if field_value.value else ""
                    confidence = getattr(field_value, 'confidence', 0.0)
                    bbox = []
                    if hasattr(field_value, 'bounding_regions') and field_value.bounding_regions:
                        bbox = [
                            coord
                            for region in field_value.bounding_regions
                            for coord in [
                                region.polygon[0].x, region.polygon[0].y,
                                region.polygon[2].x, region.polygon[2].y,
                            ]
                        ]
                    pairs.append(KeyValue(
                        key=field_name,
                        value=value_str,
                        confidence=confidence,
                        bounding_box=bbox,
                    ))
    page_count = 0
    if hasattr(result, 'pages') and result.pages:
        page_count = len(result.pages)
    return KeyValueResponse(pairs=pairs, page_count=page_count)
