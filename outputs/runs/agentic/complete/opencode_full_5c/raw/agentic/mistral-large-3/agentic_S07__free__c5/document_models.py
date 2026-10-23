from typing import Dict, List, Optional
from pydantic import BaseModel


class BoundingBox(BaseModel):
    vertices: List[Dict[str, float]]


class TextBlock(BaseModel):
    text: str
    bounding_box: BoundingBox


class OCRResponse(BaseModel):
    text: str
    blocks: List[TextBlock]


class LayoutBlock(BaseModel):
    text: str
    bounding_box: BoundingBox
    block_type: Optional[str] = None


class LayoutResponse(BaseModel):
    blocks: List[LayoutBlock]
    paragraphs: List[TextBlock]
    lines: List[TextBlock]


class TableCell(BaseModel):
    text: str
    row_index: int
    column_index: int
    bounding_box: List[Dict[str, float]]


class TableRow(BaseModel):
    cells: List[TableCell]


class DocumentTable(BaseModel):
    row_count: int
    column_count: int
    rows: List[TableRow]
    bounding_box: List[Dict[str, float]]


class TableResponse(BaseModel):
    tables: List[DocumentTable]


class KeyValuePair(BaseModel):
    key: str
    value: str
    confidence: float
    key_bounding_box: List[Dict[str, float]]
    value_bounding_box: List[Dict[str, float]]


class KeyValueResponse(BaseModel):
    key_value_pairs: List[KeyValuePair]


class FieldExtractionResponse(BaseModel):
    fields: Dict[str, str]
    confidence_scores: Dict[str, float]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    sections: List[str]
