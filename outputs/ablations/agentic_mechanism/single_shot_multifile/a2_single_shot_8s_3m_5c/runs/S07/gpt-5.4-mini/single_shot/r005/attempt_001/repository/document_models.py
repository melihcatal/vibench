from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from google.cloud import documentai


@dataclass
class DocumentRequest:
    content: Optional[bytes] = None
    content_b64: Optional[str] = None
    gcs_uri: Optional[str] = None
    mime_type: str = "image/png"
    processor_id: Optional[str] = None
    location: Optional[str] = None
    project_id: Optional[str] = None


@dataclass
class OCRResponse:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Any] = None


@dataclass
class LayoutResponse:
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    lines: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Any] = None


@dataclass
class TableResponse:
    tables: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Any] = None


@dataclass
class KeyValueResponse:
    pairs: Dict[str, str] = field(default_factory=dict)
    raw: Optional[Any] = None


@dataclass
class TranslationResponse:
    translated_text: str
    raw: Optional[Any] = None


@dataclass
class SafetyResponse:
    safe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Optional[Any] = None


@dataclass
class FieldExtractionResponse:
    fields: Dict[str, Any] = field(default_factory=dict)
    raw: Optional[Any] = None


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]] = field(default_factory=list)
    raw: Optional[Any] = None


def page_to_dict(page: documentai.Document.Page) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "page_number": page.page_number,
        "dimension": {
            "width": page.dimension.width,
            "height": page.dimension.height,
            "unit": page.dimension.unit,
        },
    }
    if page.layout and page.layout.text_anchor and page.layout.text_anchor.text_segments:
        out["text"] = ""
    return out


def text_from_document(doc: documentai.Document) -> str:
    return doc.text or ""


def kv_pairs_from_document(doc: documentai.Document) -> Dict[str, str]:
    pairs: Dict[str, str] = {}
    for page in doc.pages:
        for form_field in page.form_fields:
            key = _text_from_anchor(doc.text, form_field.field_name.text_anchor)
            value = _text_from_anchor(doc.text, form_field.field_value.text_anchor)
            if key:
                pairs[key.strip()] = value.strip()
    return pairs


def _text_from_anchor(full_text: str, text_anchor: Any) -> str:
    if not full_text or text_anchor is None:
        return ""
    segments = getattr(text_anchor, "text_segments", [])
    pieces: List[str] = []
    for seg in segments:
        start = getattr(seg, "start_index", 0) or 0
        end = getattr(seg, "end_index", 0) or 0
        pieces.append(full_text[start:end])
    return "".join(pieces)
