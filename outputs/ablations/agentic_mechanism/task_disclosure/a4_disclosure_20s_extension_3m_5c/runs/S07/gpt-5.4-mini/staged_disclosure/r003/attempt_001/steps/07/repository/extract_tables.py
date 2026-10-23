import base64
import json
import os
from typing import Any, Dict, List, Optional

import requests


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"].rstrip("/")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
AZURE_DOCUMENT_INTELLIGENCE_API_VERSION = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_API_VERSION", "2024-11-30")
AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-layout")


def _headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": AZURE_DOCUMENT_INTELLIGENCE_KEY,
    }


def _submit_document(content: bytes) -> str:
    payload = {"base64Source": base64.b64encode(content).decode("ascii")}
    url = (
        f"{AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT}/documentintelligence/documentModels/"
        f"{AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID}:analyze?api-version={AZURE_DOCUMENT_INTELLIGENCE_API_VERSION}"
    )
    response = requests.post(url, headers=_headers(), json=payload, timeout=120)
    response.raise_for_status()
    operation_url = response.headers.get("operation-location") or response.headers.get("Operation-Location")
    if not operation_url:
        raise RuntimeError("Azure Document Intelligence did not return an operation-location header")
    return operation_url


def _poll_result(operation_url: str) -> Dict[str, Any]:
    while True:
        response = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": AZURE_DOCUMENT_INTELLIGENCE_KEY}, timeout=120)
        response.raise_for_status()
        result = response.json()
        status = result.get("status")
        if status in {"succeeded", "failed"}:
            if status == "failed":
                raise RuntimeError(json.dumps(result, ensure_ascii=False))
            return result


def extract_tables(document_path: str) -> List[Dict[str, Any]]:
    with open(document_path, "rb") as f:
        operation_url = _submit_document(f.read())
    result = _poll_result(operation_url)
    analyze_result = result.get("analyzeResult", {})
    tables = analyze_result.get("tables", [])
    pages = analyze_result.get("pages", [])
    lines_by_page = {}
    for page in pages:
        page_number = page.get("pageNumber")
        lines_by_page[page_number] = page.get("lines", [])
    extracted = []
    for table in tables:
        cells = []
        for cell in table.get("cells", []):
            cells.append({
                "row_index": cell.get("rowIndex"),
                "column_index": cell.get("columnIndex"),
                "row_span": cell.get("rowSpan", 1),
                "column_span": cell.get("columnSpan", 1),
                "kind": cell.get("kind"),
                "content": cell.get("content", ""),
            })
        extracted.append({
            "row_count": table.get("rowCount"),
            "column_count": table.get("columnCount"),
            "cells": cells,
            "bounding_regions": table.get("boundingRegions", []),
            "spans": table.get("spans", []),
            "lines_by_page": lines_by_page,
        })
    return extracted


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Extract table structure from a document using Azure Document Intelligence.")
    parser.add_argument("document_path")
    args = parser.parse_args()
    print(json.dumps(extract_tables(args.document_path), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
