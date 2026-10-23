import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class DocumentRequest:
    file_content: bytes
    mime_type: str


@dataclasses.dataclass
class TextSpan:
    offset: int
    length: int


@dataclasses.dataclass
class BoundingPoly:
    vertices: List[Dict[str, float]]


@dataclasses.dataclass
class TextAnchor:
    text_segments: List[TextSpan]


@dataclasses.dataclass
class DocumentPageBlock:
    bounding_poly: BoundingPoly
    text_anchor: TextAnchor
    type: str  # e.g., "paragraph", "line", "word"


@dataclasses.dataclass
class DocumentPageTableProperty:
    text_anchor: TextAnchor
    bounding_poly: BoundingPoly
    num_rows: int
    num_columns: int
    cells: List[Dict[str, Any]]  # Simplified for now


@dataclasses.dataclass
class DocumentPageFormProperty:
    field_name: TextAnchor
    field_value: TextAnchor
    bounding_poly: BoundingPoly


@dataclasses.dataclass
class DocumentPage:
    page_number: int
    image_width: int
    image_height: int
    text: str
    blocks: List[DocumentPageBlock]
    tables: List[DocumentPageTableProperty]
    form_fields: List[DocumentPageFormProperty]


@dataclasses.dataclass
class DocumentResponse:
    text: str
    pages: List[DocumentPage]
    entities: List[Dict[str, Any]]  # For key-value pairs or structured entities
