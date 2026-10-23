from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    file_path: str


@dataclass
class TextExtractionResult:
    text: str
    pages: List[Dict[str, Any]]


@dataclass
class LayoutExtractionResult:
    elements: List[Dict[str, Any]]


@dataclass
class TableExtractionResult:
    tables: List[Dict[str, Any]]


@dataclass
class KeyValueExtractionResult:
    pairs: List[Dict[str, Optional[str]]]


def normalize_content(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value)


def normalize_document_result(result):
    pages = []
    for page in getattr(result, "pages", []) or []:
        pages.append(
            {
                "page_number": getattr(page, "page_number", None),
                "width": getattr(page, "width", None),
                "height": getattr(page, "height", None),
            }
        )
    return pages
