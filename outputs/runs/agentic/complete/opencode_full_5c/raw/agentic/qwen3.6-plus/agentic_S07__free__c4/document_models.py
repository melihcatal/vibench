from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OcrTextRequest:
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    language: str = "en"
    confidence_threshold: float = 0.0


@dataclass
class OcrTextResponse:
    text: str = ""
    confidence: float = 0.0
    page_count: int = 0
    blocks: list = field(default_factory=list)


@dataclass
class LayoutBlock:
    block_type: str = ""
    text: str = ""
    confidence: float = 0.0
    geometry: dict = field(default_factory=dict)
    page: int = 0
    children: list = field(default_factory=list)


@dataclass
class LayoutElement:
    element_type: str = ""
    text: str = ""
    confidence: float = 0.0
    bounding_box: dict = field(default_factory=dict)
    page: int = 0


@dataclass
class LayoutResponse:
    blocks: list = field(default_factory=list)
    tables: list = field(default_factory=list)
    figures: list = field(default_factory=list)
    headers: list = field(default_factory=list)
    paragraphs: list = field(default_factory=list)
    page_count: int = 0


@dataclass
class TableCell:
    row_index: int = 0
    column_index: int = 0
    text: str = ""
    confidence: float = 0.0
    is_header: bool = False
    column_span: int = 1
    row_span: int = 1
    geometry: dict = field(default_factory=dict)


@dataclass
class TableStructure:
    table_id: str = ""
    rows: list = field(default_factory=list)
    columns: list = field(default_factory=list)
    cells: list = field(default_factory=list)
    row_count: int = 0
    column_count: int = 0
    confidence: float = 0.0
    page: int = 0


@dataclass
class TableResponse:
    tables: list = field(default_factory=list)
    table_count: int = 0
    page_count: int = 0


@dataclass
class KeyValue:
    key: str = ""
    value: str = ""
    key_confidence: float = 0.0
    value_confidence: float = 0.0
    key_geometry: dict = field(default_factory=dict)
    value_geometry: dict = field(default_factory=dict)
    page: int = 0


@dataclass
class KeyValueResponse:
    key_values: list = field(default_factory=list)
    count: int = 0
    page_count: int = 0


def normalize_text_response(
    textract_response: dict, confidence_threshold: float = 0.0
) -> OcrTextResponse:
    blocks = textract_response.get("blocks", [])
    text_parts = []
    total_confidence = 0.0
    count = 0
    for block in blocks:
        if block.get("BlockType") == "LINE":
            text = block.get("Text", "")
            conf = block.get("Confidence", 0.0)
            if conf >= confidence_threshold:
                text_parts.append(text)
                total_confidence += conf
                count += 1
    avg_confidence = total_confidence / count if count > 0 else 0.0
    return OcrTextResponse(
        text="\n".join(text_parts),
        confidence=avg_confidence,
        page_count=1,
        blocks=blocks,
    )


def normalize_layout_response(textract_response: dict) -> LayoutResponse:
    blocks = textract_response.get("blocks", [])
    layout_blocks = []
    tables = []
    figures = []
    headers = []
    paragraphs = []
    for block in blocks:
        block_type = block.get("BlockType", "")
        if block_type in (
            "WORD",
            "LINE",
            "CELL",
            "TABLE",
            "KEY_VALUE_SET",
            "PAGE",
            "LAYOUT_FIGURE",
            "LAYOUT_HEADER",
            "LAYOUT_PARAGRAPH",
            "LAYOUT_TEXT",
            "LAYOUT_LIST",
            "LAYOUT_SECTION_HEADER",
            "LAYOUT_FOOTER",
        ):
            layout_block = LayoutBlock(
                block_type=block_type,
                text=block.get("Text", ""),
                confidence=block.get("Confidence", 0.0),
                geometry=block.get("Geometry", {}),
                page=block.get("Page", 0),
            )
            layout_blocks.append(layout_block)
            if block_type == "TABLE":
                tables.append(layout_block)
            elif block_type == "LAYOUT_FIGURE":
                figures.append(layout_block)
            elif block_type in ("LAYOUT_HEADER", "LAYOUT_SECTION_HEADER"):
                headers.append(layout_block)
            elif block_type in ("LAYOUT_PARAGRAPH", "LAYOUT_TEXT"):
                paragraphs.append(layout_block)
    return LayoutResponse(
        blocks=layout_blocks,
        tables=tables,
        figures=figures,
        headers=headers,
        paragraphs=paragraphs,
        page_count=1,
    )


def normalize_table_response(textract_response: dict) -> TableResponse:
    blocks = textract_response.get("blocks", [])
    block_map = textract_response.get("block_map", {})
    tables = []
    for block in blocks:
        if block.get("BlockType") == "TABLE":
            cells = []
            relationships = block.get("Relationships", [])
            for rel in relationships:
                if rel.get("Type") == "CHILD":
                    for child_id in rel.get("Ids", []):
                        child_block = block_map.get(child_id, {})
                        if child_block.get("BlockType") == "CELL":
                            cell = TableCell(
                                row_index=child_block.get("RowIndex", 0),
                                column_index=child_block.get("ColumnIndex", 0),
                                text=child_block.get("Text", ""),
                                confidence=child_block.get("Confidence", 0.0),
                                is_header=child_block.get("IsHeaderCell", False),
                                column_span=child_block.get("ColumnSpan", 1),
                                row_span=child_block.get("RowSpan", 1),
                                geometry=child_block.get("Geometry", {}),
                            )
                            cells.append(cell)
            row_indices = {c.row_index for c in cells}
            col_indices = {c.column_index for c in cells}
            table = TableStructure(
                table_id=block.get("Id", ""),
                cells=cells,
                row_count=max(row_indices) if row_indices else 0,
                column_count=max(col_indices) if col_indices else 0,
                confidence=block.get("Confidence", 0.0),
                page=block.get("Page", 0),
            )
            tables.append(table)
    return TableResponse(
        tables=tables,
        table_count=len(tables),
        page_count=1,
    )


def normalize_kv_response(textract_response: dict) -> KeyValueResponse:
    blocks = textract_response.get("blocks", [])
    block_map = textract_response.get("block_map", {})
    key_values = []
    for block in blocks:
        if block.get("BlockType") == "KEY_VALUE_SET":
            entity_types = block.get("EntityTypes", [])
            if "KEY" in entity_types:
                key_text = block.get("Text", "")
                key_confidence = block.get("Confidence", 0.0)
                key_geometry = block.get("Geometry", {})
                value_text = ""
                value_confidence = 0.0
                value_geometry = {}
                relationships = block.get("Relationships", [])
                for rel in relationships:
                    if rel.get("Type") == "VALUE":
                        for value_id in rel.get("Ids", []):
                            value_block = block_map.get(value_id, {})
                            value_text = value_block.get("Text", "")
                            value_confidence = value_block.get("Confidence", 0.0)
                            value_geometry = value_block.get("Geometry", {})
                kv = KeyValue(
                    key=key_text,
                    value=value_text,
                    key_confidence=key_confidence,
                    value_confidence=value_confidence,
                    key_geometry=key_geometry,
                    value_geometry=value_geometry,
                    page=block.get("Page", 0),
                )
                key_values.append(kv)
    return KeyValueResponse(
        key_values=key_values,
        count=len(key_values),
        page_count=1,
    )
