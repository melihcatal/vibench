from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class OCRResult:
    text: str
    pages: List[Dict[str, Any]]
    raw: Any = None


@dataclass
class LayoutElement:
    kind: str
    text: str
    polygon: Optional[List[float]] = None
    raw: Any = None


@dataclass
class TableCell:
    row_index: int
    column_index: int
    text: str
    row_span: int = 1
    column_span: int = 1
    raw: Any = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    raw: Any = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def page_dict(page: Any) -> Dict[str, Any]:
    return {
        "page_number": getattr(page, "page_number", None),
        "width": getattr(page, "width", None),
        "height": getattr(page, "height", None),
    }
