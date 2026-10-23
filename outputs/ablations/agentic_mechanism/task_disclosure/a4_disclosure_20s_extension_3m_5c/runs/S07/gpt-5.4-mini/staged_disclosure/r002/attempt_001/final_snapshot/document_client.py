import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").rstrip("/")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
AZURE_DOCUMENT_INTELLIGENCE_API_VERSION = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2023-10-31-preview")
AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL_ID = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL_ID", "prebuilt-read")
AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL_ID = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL_ID", "prebuilt-layout")


class DocumentClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class DocumentClientConfig:
    endpoint: str = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    key: str = AZURE_DOCUMENT_INTELLIGENCE_KEY
    api_version: str = AZURE_DOCUMENT_INTELLIGENCE_API_VERSION
    ocr_model_id: str = AZURE_DOCUMENT_INTELLIGENCE_OCR_MODEL_ID
    layout_model_id: str = AZURE_DOCUMENT_INTELLIGENCE_LAYOUT_MODEL_ID


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig()


def _require(value: str, name: str) -> str:
    if not value:
        raise DocumentClientError(f"{name} is required")
    return value


def _headers(config: DocumentClientConfig) -> Dict[str, str]:
    return {"Ocp-Apim-Subscription-Key": _require(config.key, "AZURE_DOCUMENT_INTELLIGENCE_KEY")}


def _analyze_url(config: DocumentClientConfig, model_id: str) -> str:
    endpoint = _require(config.endpoint, "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    return f"{endpoint}/formrecognizer/documentModels/{model_id}:analyze?api-version={config.api_version}"


def _poll_operation(operation_url: str, config: DocumentClientConfig) -> Dict[str, Any]:
    while True:
        response = requests.get(operation_url, headers=_headers(config), timeout=60)
        if response.status_code != 200:
            raise DocumentClientError(f"Polling failed: {response.status_code} {response.text}")
        payload = response.json()
        status = payload.get("status")
        if status in {"succeeded", "failed", "canceled"}:
            if status != "succeeded":
                raise DocumentClientError(f"Analysis {status}: {payload}")
            return payload.get("analyzeResult", payload)


def analyze_document(document_url: str, model_id: str) -> Dict[str, Any]:
    config = load_config()
    response = requests.post(
        _analyze_url(config, model_id),
        headers={**_headers(config), "Content-Type": "application/json"},
        json={"urlSource": document_url},
        timeout=60,
    )
    if response.status_code not in (200, 202):
        raise DocumentClientError(f"Analyze request failed: {response.status_code} {response.text}")
    operation_url = response.headers.get("operation-location") or response.headers.get("Operation-Location")
    if not operation_url:
        raise DocumentClientError("Missing operation-location header from Azure Document Intelligence")
    return _poll_operation(operation_url, config)


def extract_ocr(document_url: str) -> Dict[str, Any]:
    return analyze_document(document_url, load_config().ocr_model_id)


def extract_layout(document_url: str) -> Dict[str, Any]:
    return analyze_document(document_url, load_config().layout_model_id)


def collect_ocr_text(result: Dict[str, Any]) -> str:
    lines = []
    for page in result.get("pages", []):
        for line in page.get("lines", []):
            content = line.get("content")
            if content:
                lines.append(content)
    if lines:
        return "\n".join(lines)
    return result.get("content", "") or ""


def collect_layout_items(result: Dict[str, Any]) -> Dict[str, Any]:
    blocks = []
    lines = []
    tables = []
    elements = []
    for page in result.get("pages", []):
        for line in page.get("lines", []):
            lines.append({"page": page.get("pageNumber"), **line})
        for word in page.get("words", []):
            blocks.append({"page": page.get("pageNumber"), **word})
    for table in result.get("tables", []):
        tables.append(table)
    for paragraph in result.get("paragraphs", []):
        elements.append(paragraph)
    if not blocks and not lines and not tables and not elements:
        content = result.get("content")
        if content:
            elements.append({"content": content})
    return {"blocks": blocks, "lines": lines, "tables": tables, "layout_elements": elements}


def extract_ocr_text_from_url(document_url: str) -> str:
    return collect_ocr_text(extract_ocr(document_url))


def extract_layout_from_url(document_url: str) -> Dict[str, Any]:
    return collect_layout_items(extract_layout(document_url))
