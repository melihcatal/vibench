from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class DocumentTextExtractionResponse:
    text: str
    document_id: str = ""

@dataclass
class DocumentLayoutElement:
    text_content: str
    page_number: int
    bounding_boxes: List[Any] = field(default_factory=list) # simplified

@dataclass
class DocumentLayoutExtractionResponse:
    pages: List[Dict[str, Any]] = field(default_factory=list)
    document_id: str = ""

@dataclass
class DocumentTable:
    page_number: int
    full_text_content: str
    # More detailed table structure could be added here
    # e.g., rows: List[List[str]]

@dataclass
class DocumentTableExtractionResponse:
    tables: List[DocumentTable] = field(default_factory=list)
    document_id: str = ""

@dataclass
class DocumentKeyValuePair:
    key: str
    value: str
    page_number: int = None

@dataclass
class DocumentKeyValuePairExtractionResponse:
    key_value_pairs: List[DocumentKeyValuePair] = field(default_factory=list)
    document_id: str = ""

# Although not strictly used by the current Document AI SDK calls directly
# these models provide a structured way to represent and normalize outputs
# for downstream processing or custom API wrappers.
