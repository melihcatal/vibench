from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class DocumentRequest:
    project_id: str
    location: str
    processor_id: str
    file_content: bytes
    mime_type: str


@dataclass
class LayoutExtractionResponse:
    text: str
    pages: List[Dict[str, Any]]


@dataclass
class Table:
    rows: List[List[str]]


@dataclass
class TableExtractionResponse:
    tables: List[Table]


@dataclass
class KeyValueExtractionResponse:
    key_values: Dict[str, str]
