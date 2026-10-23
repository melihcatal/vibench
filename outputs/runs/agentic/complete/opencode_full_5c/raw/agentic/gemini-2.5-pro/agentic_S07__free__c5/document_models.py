from pydantic import BaseModel
from typing import List, Optional


class Point(BaseModel):
    x: float
    y: float


class BoundingBox(BaseModel):
    points: List[Point]
    text: Optional[str] = None


class Line(BaseModel):
    text: str
    bounding_box: BoundingBox


class Block(BaseModel):
    text: str
    bounding_box: BoundingBox
    lines: List[Line]


class TableCell(BaseModel):
    text: str
    row_index: int
    column_index: int
    bounding_box: BoundingBox


class Table(BaseModel):
    cells: List[TableCell]
    row_count: int
    column_count: int
    bounding_box: BoundingBox


class KeyValuePair(BaseModel):
    key: str
    value: str
    confidence: float


class DocumentLayout(BaseModel):
    blocks: List[Block]
    tables: List[Table]


class ExtractedText(BaseModel):
    text: str


class ExtractedTables(BaseModel):
    tables: List[Table]


class ExtractedKeyValues(BaseModel):
    key_values: List[KeyValuePair]


class TranslatedText(BaseModel):
    translated_text: str
    source_language: str


class SafetyResult(BaseModel):
    is_safe: bool
    confidence: float


class ExtractedFields(BaseModel):
    fields: dict


class DocumentEmbedding(BaseModel):
    embedding: List[float]
    model: str
