from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class DocumentType(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"
    FORM = "form"
    CONTRACT = "contract"
    GENERIC = "generic"


class LayoutBlockType(str, Enum):
    TEXT = "TEXT"
    HEADING = "HEADING"
    LIST = "LIST"
    TABLE = "TABLE"
    IMAGE = "IMAGE"
    FORM_FIELD = "FORM_FIELD"
    SIGNATURE = "SIGNATURE"


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    @classmethod
    def from_vertices(cls, vertices: List[Dict[str, float]]) -> "BoundingBox":
        xs = [v["x"] for v in vertices]
        ys = [v["y"] for v in vertices]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return cls(x=min_x, y=min_y, width=max_x - min_x, height=max_y - min_y)


@dataclass
class OCRTextRequest:
    image_bytes: bytes
    mime_type: str = "image/png"
    language_hint: Optional[str] = None
    enable_text_detection: bool = True
    enable_document_text: bool = True


@dataclass
class OCRTextResponse:
    text: str
    confidence: float
    language: Optional[str] = None
    page_count: int = 1
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class LayoutBlock:
    text: str
    block_type: str
    confidence: float
    bounding_box: BoundingBox
    children: List["LayoutBlock"] = field(default_factory=list)


@dataclass
class LayoutRequest:
    image_bytes: bytes
    mime_type: str = "image/png"
    include_tables: bool = True
    include_forms: bool = True
    include_entities: bool = True


@dataclass
class LayoutResponse:
    blocks: List[LayoutBlock]
    page_count: int = 1
    tables: List[List[List[Dict[str, Any]]]] = field(default_factory=list)
    key_values: List[Dict[str, str]] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TableRequest:
    image_bytes: bytes
    mime_type: str = "image/png"
    detect_headers: bool = True


@dataclass
class TableCell:
    text: str
    row_index: int
    col_index: int
    row_span: int = 1
    col_span: int = 1
    confidence: float = 1.0


@dataclass
class TableRow:
    cells: List[TableCell]
    is_header: bool = False


@dataclass
class TableResponse:
    tables: List[List[TableRow]]
    table_count: int = 0
    raw_response: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.table_count == 0:
            self.table_count = len(self.tables)


@dataclass
class KeyValueRequest:
    image_bytes: bytes
    mime_type: str = "image/png"
    form_type: Optional[str] = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None


@dataclass
class KeyValueResponse:
    pairs: List[KeyValuePair]
    form_fields_detected: int = 0
    raw_response: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.form_fields_detected == 0:
            self.form_fields_detected = len(self.pairs)


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    format: str = "text"


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SafetyRequest:
    text: str
    categories: Optional[List[str]] = None


@dataclass
class SafetyCategory:
    name: str
    score: float
    is_flagged: bool


@dataclass
class SafetyResponse:
    overall_safe: bool
    categories: List[SafetyCategory]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class FieldExtractionRequest:
    text: str
    schema: Dict[str, Any]
    extraction_model: str = "gpt-4o"


@dataclass
class FieldExtractionResponse:
    extracted_fields: Dict[str, Any]
    confidence: float
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-3-large"
    dimensions: Optional[int] = None


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str
    usage: Dict[str, int] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None


def normalize_ocr_response(vision_response) -> OCRTextResponse:
    text_parts = []
    total_confidence = 0.0
    count = 0
    for resp in vision_response.responses:
        if resp.full_text_annotation:
            text_parts.append(resp.full_text_annotation.text)
            for page in resp.full_text_annotation.pages:
                for block in page.blocks:
                    total_confidence += block.confidence
                    count += 1
    avg_confidence = total_confidence / count if count > 0 else 0.0
    return OCRTextResponse(
        text="\n".join(filter(None, text_parts)),
        confidence=avg_confidence,
    )


def normalize_layout_response(blocks_data: List[Dict]) -> LayoutResponse:
    layout_blocks = []
    for block_data in blocks_data:
        vertices = block_data.get("bounding_box", [])
        bbox = (
            BoundingBox.from_vertices(vertices) if vertices else BoundingBox(0, 0, 0, 0)
        )
        layout_blocks.append(
            LayoutBlock(
                text=block_data.get("text", ""),
                block_type=block_data.get("block_type", "TEXT"),
                confidence=block_data.get("confidence", 1.0),
                bounding_box=bbox,
            )
        )
    return LayoutResponse(blocks=layout_blocks)


def normalize_table_response(tables_data: List[List[List[Dict]]]) -> TableResponse:
    tables = []
    for table_data in tables_data:
        rows = []
        for row_idx, row_data in enumerate(table_data):
            cells = []
            for col_idx, cell_data in enumerate(row_data):
                cells.append(
                    TableCell(
                        text=cell_data.get("text", ""),
                        row_index=row_idx,
                        col_index=col_idx,
                        row_span=cell_data.get("row_span", 1),
                        col_span=cell_data.get("col_span", 1),
                        confidence=cell_data.get("confidence", 1.0),
                    )
                )
            rows.append(TableRow(cells=cells, is_header=(row_idx == 0)))
        tables.append(rows)
    return TableResponse(tables=tables)


def normalize_kv_response(kv_data: List[Dict]) -> KeyValueResponse:
    pairs = []
    for item in kv_data:
        pairs.append(
            KeyValuePair(
                key=item.get("key", ""),
                value=item.get("value", ""),
                confidence=item.get("confidence", 1.0),
            )
        )
    return KeyValueResponse(pairs=pairs)
