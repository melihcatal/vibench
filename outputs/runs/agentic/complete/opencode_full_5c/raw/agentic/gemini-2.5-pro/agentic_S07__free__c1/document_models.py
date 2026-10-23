from pydantic import BaseModel, Field
from typing import List, Optional


class Point(BaseModel):
    x: float
    y: float


class BoundingRegion(BaseModel):
    page_number: int
    polygon: List[Point]


class Span(BaseModel):
    offset: int
    length: int


class Block(BaseModel):
    content: str
    bounding_regions: List[BoundingRegion]
    spans: List[Span]


class Line(BaseModel):
    content: str
    polygon: List[Point]
    spans: List[Span]


class TableCell(BaseModel):
    kind: str
    content: str
    bounding_regions: List[BoundingRegion]
    spans: List[Span]
    row_index: int
    column_index: int
    row_span: Optional[int] = 1
    column_span: Optional[int] = 1


class Table(BaseModel):
    row_count: int
    column_count: int
    cells: List[TableCell]
    bounding_regions: List[BoundingRegion]
    spans: List[Span]


class KeyValue(BaseModel):
    content: str
    spans: List[Span]


class KeyValuePair(BaseModel):
    key: KeyValue
    value: Optional[KeyValue]
    confidence: float
