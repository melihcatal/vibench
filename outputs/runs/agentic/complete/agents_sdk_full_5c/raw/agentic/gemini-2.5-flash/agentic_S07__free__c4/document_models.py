from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ExtractedTextResult:
    text: str

@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

@dataclass
class LayoutElement:
    type: str # e.g., "paragraph", "line", "table", "form_field"
    text: str
    bounding_boxes: List[BoundingBox]
    # Additional fields like confidence, page number can be added

@dataclass
class TableCell:
    row_idx: int
    col_idx: int
    text: str
    bounding_boxes: List[BoundingBox]
    header_cell: bool = False

@dataclass
class ExtractedTable:
    cells: List[TableCell]
    num_rows: int
    num_cols: int
    bounding_boxes: List[BoundingBox]

@dataclass
class KeyValueEntry:
    key: str
    value: str
    key_bounding_boxes: List[BoundingBox]
    value_bounding_boxes: List[BoundingBox]

@dataclass
class DocumentProcessingRequest:
    image_content: bytes
    mime_type: str = "application/pdf"
    # Potentially other common parameters like `processor_id`, `project_id`, `location`

@dataclass
class DocumentProcessingResponse:
    document_text: str = ""
    layout_elements: List[LayoutElement] = field(default_factory=list)
    tables: List[ExtractedTable] = field(default_factory=list)
    key_value_pairs: List[KeyValueEntry] = field(default_factory=list)
    raw_response: Optional[Any] = None # To hold the original provider response if needed


if __name__ == '__main__':
    _bbox = BoundingBox(x_min=0.1, y_min=0.1, x_max=0.2, y_max=0.2)
    _text_result = ExtractedTextResult(text="Hello World")
    _layout_element = LayoutElement(type="paragraph", text="Some text", bounding_boxes=[_bbox])
    _cell = TableCell(row_idx=0, col_idx=0, text="Header 1", header_cell=True, bounding_boxes=[_bbox])
    _table = ExtractedTable(cells=[_cell], num_rows=1, num_cols=1, bounding_boxes=[_bbox])
    _kv_entry = KeyValueEntry(key="Name", value="John Doe", key_bounding_boxes=[_bbox], value_bounding_boxes=[_bbox])

    _response = DocumentProcessingResponse(
        document_text=_text_result.text,
        layout_elements=[_layout_element],
        tables=[_table],
        key_value_pairs=[_kv_entry]
    )
    print(f"Sample DocumentProcessingResponse: {len(_response.tables)} tables, {len(_response.key_value_pairs)} KVs")
