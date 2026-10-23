from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCRRequest:
    document_path: str
    project_id: Optional[str] = None
    location: Optional[str] = None
    processor_id: Optional[str] = None


@dataclass
class OCRResponse:
    text: str = ''
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutResponse:
    elements: List[Dict[str, Any]] = field(default_factory=list)
    text: str = ''


@dataclass
class TableResponse:
    tables: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class KeyValueResponse:
    key_values: List[Dict[str, Any]] = field(default_factory=list)


def normalize_text(data: Dict[str, Any]) -> OCRResponse:
    return OCRResponse(text=data.get('text', ''), payload=data)


def normalize_layout(data: Dict[str, Any]) -> LayoutResponse:
    return LayoutResponse(elements=data.get('elements', []), text=data.get('text', ''))


def normalize_tables(data: Dict[str, Any]) -> TableResponse:
    return TableResponse(tables=data.get('tables', []))


def normalize_key_values(data: Dict[str, Any]) -> KeyValueResponse:
    return KeyValueResponse(key_values=data.get('key_values', []))
