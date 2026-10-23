from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    image_bytes: bytes
    content_type: str = "application/octet-stream"


@dataclass
class TextExtractionResult:
    text: str
    operation_location: str = ""
    status_code: int = 0


@dataclass
class LayoutExtractionResult:
    elements: List[Dict[str, Any]]
    operation_location: str = ""
    status_code: int = 0


@dataclass
class TableExtractionResult:
    tables: List[Dict[str, Any]]
    operation_location: str = ""
    status_code: int = 0


@dataclass
class KeyValueExtractionResult:
    key_values: List[Dict[str, Any]]
    operation_location: str = ""
    status_code: int = 0


def _operation_location(payload: Dict[str, Any]) -> str:
    return payload.get("operation_location", payload.get("operation-location", ""))


def normalize_text_response(payload: Dict[str, Any]) -> TextExtractionResult:
    return TextExtractionResult(text=str(payload.get("text", "")), operation_location=_operation_location(payload), status_code=int(payload.get("status_code", 0)))


def normalize_layout_response(payload: Dict[str, Any]) -> LayoutExtractionResult:
    return LayoutExtractionResult(elements=list(payload.get("elements", [])), operation_location=_operation_location(payload), status_code=int(payload.get("status_code", 0)))


def normalize_table_response(payload: Dict[str, Any]) -> TableExtractionResult:
    return TableExtractionResult(tables=list(payload.get("tables", [])), operation_location=_operation_location(payload), status_code=int(payload.get("status_code", 0)))


def normalize_key_value_response(payload: Dict[str, Any]) -> KeyValueExtractionResult:
    return KeyValueExtractionResult(key_values=list(payload.get("key_values", [])), operation_location=_operation_location(payload), status_code=int(payload.get("status_code", 0)))
