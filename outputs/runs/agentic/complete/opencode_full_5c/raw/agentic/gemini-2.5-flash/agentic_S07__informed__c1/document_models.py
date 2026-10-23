from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class DocumentTextExtractionResponse:
    text: str


@dataclass
class DocumentLayoutResponse:
    pages: List[Dict[str, Any]]


@dataclass
class DocumentTableResponse:
    tables: List[Dict[str, Any]]


@dataclass
class DocumentKeyValueResponse:
    key_value_pairs: List[Dict[str, str]]


@dataclass
class DocumentProcessRequest:
    project_id: str
    location: str
    processor_id: str
    file_content: bytes
    mime_type: str
