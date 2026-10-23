from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    image_url: Optional[str] = None
    image_bytes_b64: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class LayoutRequest:
    image_url: Optional[str] = None
    image_bytes_b64: Optional[str] = None
    features: List[str] = field(default_factory=list)


@dataclass
class TableRequest:
    image_url: Optional[str] = None
    image_bytes_b64: Optional[str] = None


@dataclass
class KeyValueRequest:
    image_url: Optional[str] = None
    image_bytes_b64: Optional[str] = None


@dataclass
class OCRResponse:
    text: str
    raw: Dict[str, Any]


@dataclass
class LayoutResponse:
    blocks: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class TableResponse:
    tables: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class KeyValueResponse:
    key_values: Dict[str, str]
    raw: Dict[str, Any]


def normalize_document_result(raw: Dict[str, Any]) -> Dict[str, Any]:
    pages = raw.get("pages", []) or raw.get("analyzeResult", {}).get("pages", [])
    paragraphs = raw.get("paragraphs", []) or raw.get("analyzeResult", {}).get("paragraphs", [])
    tables = raw.get("tables", []) or raw.get("analyzeResult", {}).get("tables", [])
    key_value_pairs = raw.get("keyValuePairs", []) or raw.get("analyzeResult", {}).get("keyValuePairs", [])
    return {
        "pages": pages,
        "paragraphs": paragraphs,
        "tables": tables,
        "keyValuePairs": key_value_pairs,
        "raw": raw,
    }
