from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DocumentOCRRequest:
    image_bytes: bytes


@dataclass
class DocumentLayoutRequest:
    image_bytes: bytes


@dataclass
class DocumentTableRequest:
    image_bytes: bytes
    processor_id: str
    location: str
    mime_type: str = "image/png"
    project_id: Optional[str] = None


@dataclass
class DocumentKVPRequest:
    image_bytes: bytes
    processor_id: str
    location: str
    mime_type: str = "image/png"
    project_id: Optional[str] = None


@dataclass
class OCRTextResponse:
    text: str
    raw: Any


@dataclass
class LayoutElement:
    kind: str
    text: str
    bbox: dict


@dataclass
class LayoutResponse:
    elements: list[LayoutElement]
    raw: Any


@dataclass
class TableCell:
    text: str
    bbox: dict


@dataclass
class TableRow:
    cells: list[TableCell]


@dataclass
class TableResponse:
    rows: list[TableRow]
    raw: Any


@dataclass
class KeyValuePair:
    key: str
    value: str
    key_bbox: dict
    value_bbox: dict


@dataclass
class KeyValueResponse:
    pairs: list[KeyValuePair]
    raw: Any


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def bbox_to_dict(bbox: Any) -> dict:
    if bbox is None:
        return {}
    vertices = getattr(bbox, "vertices", None) or []
    return {"vertices": [{"x": getattr(v, "x", None), "y": getattr(v, "y", None)} for v in vertices]}
