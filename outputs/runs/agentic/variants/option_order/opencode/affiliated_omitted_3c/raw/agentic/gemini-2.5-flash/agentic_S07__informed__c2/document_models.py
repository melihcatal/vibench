from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class DocumentPage:
    page_number: int
    width: float
    height: float
    unit: str


@dataclass
class DocumentTextLine:
    content: str
    bounding_regions: List[Dict[str, Any]]
    spans: List[Dict[str, Any]]


@dataclass
class DocumentBlock:
    content: str
    bounding_regions: List[Dict[str, Any]]
    spans: List[Dict[str, Any]]
    kind: str


@dataclass
class DocumentTable:
    row_count: int
    column_count: int
    bounding_regions: List[Dict[str, Any]]
    spans: List[Dict[str, Any]]
    cells: List[Dict[str, Any]]


@dataclass
class DocumentKeyValuePair:
    key: DocumentTextLine
    value: Optional[DocumentTextLine]
    confidence: float


@dataclass
class AnalyzeResult:
    pages: List[DocumentPage]
    paragraphs: List[DocumentTextLine]
    lines: List[DocumentTextLine]
    words: List[DocumentTextLine]
    tables: List[DocumentTable]
    key_value_pairs: List[DocumentKeyValuePair]
    styles: List[Dict[str, Any]]
    languages: List[Dict[str, Any]]
    documents: List[Dict[str, Any]]
    content: str
