from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    source: str


@dataclass
class OCRResponse:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    type: str
    text: str
    bounding_regions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str


@dataclass
class KeyValuePair:
    key: str
    value: str


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


def normalize_blocks(raw: Dict[str, Any]) -> List[LayoutElement]:
    elements: List[LayoutElement] = []
    for block in raw.get("blocks", []) or []:
        elements.append(
            LayoutElement(
                type=block.get("type", "block"),
                text=normalize_text(block.get("text")),
                bounding_regions=block.get("boundingRegions", []) or [],
            )
        )
    return elements


def normalize_tables(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    tables: List[Dict[str, Any]] = []
    for table in raw.get("tables", []) or []:
        tables.append(table)
    return tables


def normalize_key_values(raw: Dict[str, Any]) -> List[KeyValuePair]:
    pairs: List[KeyValuePair] = []
    for item in raw.get("keyValuePairs", []) or []:
        pairs.append(
            KeyValuePair(
                key=normalize_text(item.get("key")),
                value=normalize_text(item.get("value")),
            )
        )
    return pairs
