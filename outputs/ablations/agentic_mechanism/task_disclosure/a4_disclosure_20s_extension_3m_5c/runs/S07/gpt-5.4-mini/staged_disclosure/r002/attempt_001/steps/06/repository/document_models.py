import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").rstrip("/")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
AZURE_DOCUMENT_INTELLIGENCE_API_VERSION = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2023-10-31-preview")
AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL_ID = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL_ID", "prebuilt-read")
AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL_ID = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL_ID", "prebuilt-layout")


class DocumentModelError(RuntimeError):
    pass


@dataclass(frozen=True)
class OCRRequest:
    document_url: str
    model_id: str = AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL_ID
    api_version: str = AZURE_DOCUMENT_INTELLIGENCE_API_VERSION


@dataclass(frozen=True)
class LayoutRequest:
    document_url: str
    model_id: str = AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL_ID
    api_version: str = AZURE_DOCUMENT_INTELLIGENCE_API_VERSION


@dataclass(frozen=True)
class OCRResponse:
    raw: Dict[str, Any]
    text: str


@dataclass(frozen=True)
class LayoutResponse:
    raw: Dict[str, Any]
    blocks: List[Dict[str, Any]]
    lines: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    layout_elements: List[Dict[str, Any]]


def require_document_intelligence_config() -> None:
    if not AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT:
        raise DocumentModelError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
    if not AZURE_DOCUMENT_INTELLIGENCE_KEY:
        raise DocumentModelError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")


def normalize_ocr_text(result: Dict[str, Any]) -> str:
    lines: List[str] = []
    for page in result.get("pages", []):
        for line in page.get("lines", []):
            content = line.get("content")
            if content:
                lines.append(content)
    if lines:
        return "\n".join(lines)
    return result.get("content", "") or ""


def normalize_layout_result(result: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    blocks: List[Dict[str, Any]] = []
    lines: List[Dict[str, Any]] = []
    tables: List[Dict[str, Any]] = []
    layout_elements: List[Dict[str, Any]] = []

    for page in result.get("pages", []):
        for line in page.get("lines", []):
            lines.append({"page": page.get("pageNumber"), **line})
        for word in page.get("words", []):
            blocks.append({"page": page.get("pageNumber"), **word})

    for table in result.get("tables", []):
        tables.append(table)

    for paragraph in result.get("paragraphs", []):
        layout_elements.append(paragraph)

    if not blocks and not lines and not tables and not layout_elements:
        content = result.get("content")
        if content:
            layout_elements.append({"content": content})

    return {
        "blocks": blocks,
        "lines": lines,
        "tables": tables,
        "layout_elements": layout_elements,
    }


def to_ocr_response(result: Dict[str, Any]) -> OCRResponse:
    return OCRResponse(raw=result, text=normalize_ocr_text(result))


def to_layout_response(result: Dict[str, Any]) -> LayoutResponse:
    normalized = normalize_layout_result(result)
    return LayoutResponse(raw=result, **normalized)
