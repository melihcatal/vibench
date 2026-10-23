import json
import os
from typing import Any, Dict, List, Optional

import requests


AZURE_DOC_INTELLIGENCE_ENDPOINT = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").rstrip("/")
AZURE_DOC_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
AZURE_DOC_INTELLIGENCE_API_VERSION = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2023-10-31-preview")
AZURE_DOC_INTELLIGENCE_MODEL_ID = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-layout")


class LayoutExtractionError(RuntimeError):
    pass


def _headers() -> Dict[str, str]:
    if not AZURE_DOC_INTELLIGENCE_KEY:
        raise LayoutExtractionError("AZURE_DOCUMENT_INTELLIGENCE_KEY is required")
    return {
        "Ocp-Apim-Subscription-Key": AZURE_DOC_INTELLIGENCE_KEY,
    }


def _analyze_url() -> str:
    if not AZURE_DOC_INTELLIGENCE_ENDPOINT:
        raise LayoutExtractionError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required")
    return (
        f"{AZURE_DOC_INTELLIGENCE_ENDPOINT}/formrecognizer/documentModels/"
        f"{AZURE_DOC_INTELLIGENCE_MODEL_ID}:analyze?api-version={AZURE_DOC_INTELLIGENCE_API_VERSION}"
    )


def extract_layout(document_url: str) -> Dict[str, Any]:
    response = requests.post(
        _analyze_url(),
        headers={**_headers(), "Content-Type": "application/json"},
        json={"urlSource": document_url},
        timeout=60,
    )
    if response.status_code not in (202, 200):
        raise LayoutExtractionError(f"Analyze request failed: {response.status_code} {response.text}")

    operation_url = response.headers.get("operation-location") or response.headers.get("Operation-Location")
    if not operation_url:
        raise LayoutExtractionError("Missing operation-location header from Azure Document Intelligence")

    while True:
        result = requests.get(operation_url, headers=_headers(), timeout=60)
        if result.status_code != 200:
            raise LayoutExtractionError(f"Polling failed: {result.status_code} {result.text}")
        payload = result.json()
        status = payload.get("status")
        if status in {"succeeded", "failed", "canceled"}:
            if status != "succeeded":
                raise LayoutExtractionError(f"Analysis {status}: {json.dumps(payload)}")
            return payload.get("analyzeResult", payload)


def _collect_items(result: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    blocks: List[Dict[str, Any]] = []
    lines: List[Dict[str, Any]] = []
    tables: List[Dict[str, Any]] = []
    elements: List[Dict[str, Any]] = []

    for page in result.get("pages", []):
        for line in page.get("lines", []):
            lines.append({"page": page.get("pageNumber"), **line})
        for block in page.get("words", []):
            blocks.append({"page": page.get("pageNumber"), **block})

    for table in result.get("tables", []):
        tables.append(table)

    for paragraph in result.get("paragraphs", []):
        elements.append(paragraph)

    if not blocks and not lines and not tables and not elements:
        content = result.get("content")
        if content:
            elements.append({"content": content})

    return {"blocks": blocks, "lines": lines, "tables": tables, "layout_elements": elements}


def extract_layout_from_url(document_url: str) -> Dict[str, Any]:
    return _collect_items(extract_layout(document_url))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("document_url")
    args = parser.parse_args()
    print(json.dumps(extract_layout_from_url(args.document_url), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
