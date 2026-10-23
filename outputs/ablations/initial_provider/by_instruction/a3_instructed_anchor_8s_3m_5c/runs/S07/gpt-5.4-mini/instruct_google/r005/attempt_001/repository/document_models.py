from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_blocks(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for block in blocks:
        item = dict(block)
        if "text" in item:
            item["text"] = normalize_text(str(item["text"]))
        normalized.append(item)
    return normalized


@dataclass
class OCRRequest:
    image_uri: Optional[str] = None
    image_bytes: Optional[bytes] = None


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
    fields: Dict[str, Any]
    raw: Dict[str, Any]
