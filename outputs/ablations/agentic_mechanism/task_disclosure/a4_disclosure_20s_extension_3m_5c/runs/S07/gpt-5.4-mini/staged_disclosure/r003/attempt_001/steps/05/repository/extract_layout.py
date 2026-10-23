import argparse
import json
import os
from typing import Any, Dict, List, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def _client() -> DocumentIntelligenceClient:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def _serialize_span(span: Any) -> Dict[str, Any]:
    return {"offset": getattr(span, "offset", None), "length": getattr(span, "length", None)}


def _serialize_polygon(polygon: Any) -> Optional[List[float]]:
    if polygon is None:
        return None
    if isinstance(polygon, list):
        return [float(v) for v in polygon]
    try:
        return [float(v) for v in polygon]
    except TypeError:
        return None


def _serialize_layout(result: Any) -> Dict[str, Any]:
    pages = []
    for page in getattr(result, "pages", []) or []:
        pages.append(
            {
                "page_number": getattr(page, "page_number", None),
                "width": getattr(page, "width", None),
                "height": getattr(page, "height", None),
                "unit": getattr(page, "unit", None),
                "lines": [
                    {
                        "content": getattr(line, "content", None),
                        "spans": [_serialize_span(s) for s in getattr(line, "spans", []) or []],
                        "polygon": _serialize_polygon(getattr(line, "polygon", None)),
                    }
                    for line in getattr(page, "lines", []) or []
                ],
                "words": [
                    {
                        "content": getattr(word, "content", None),
                        "confidence": getattr(word, "confidence", None),
                        "span": _serialize_span(getattr(word, "span", None)) if getattr(word, "span", None) else None,
                        "polygon": _serialize_polygon(getattr(word, "polygon", None)),
                    }
                    for word in getattr(page, "words", []) or []
                ],
            }
        )

    tables = []
    for table in getattr(result, "tables", []) or []:
        tables.append(
            {
                "row_count": getattr(table, "row_count", None),
                "column_count": getattr(table, "column_count", None),
                "cells": [
                    {
                        "row_index": getattr(cell, "row_index", None),
                        "column_index": getattr(cell, "column_index", None),
                        "content": getattr(cell, "content", None),
                        "kind": getattr(cell, "kind", None),
                        "spans": [_serialize_span(s) for s in getattr(cell, "spans", []) or []],
                    }
                    for cell in getattr(table, "cells", []) or []
                ],
            }
        )

    paragraphs = []
    for para in getattr(result, "paragraphs", []) or []:
        paragraphs.append(
            {
                "content": getattr(para, "content", None),
                "role": getattr(para, "role", None),
                "spans": [_serialize_span(s) for s in getattr(para, "spans", []) or []],
            }
        )

    figures = []
    for figure in getattr(result, "figures", []) or []:
        figures.append(
            {
                "spans": [_serialize_span(s) for s in getattr(figure, "spans", []) or []],
                "bounding_regions": [
                    {
                        "page_number": getattr(br, "page_number", None),
                        "polygon": _serialize_polygon(getattr(br, "polygon", None)),
                    }
                    for br in getattr(figure, "bounding_regions", []) or []
                ],
            }
        )

    return {"pages": pages, "tables": tables, "paragraphs": paragraphs, "figures": figures}


def extract_layout(source: str) -> Dict[str, Any]:
    client = _client()
    with open(source, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-layout", analyze_request=f, content_type="application/octet-stream")
    result = poller.result()
    return _serialize_layout(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    args = parser.parse_args()
    print(json.dumps(extract_layout(args.source), ensure_ascii=False))


if __name__ == "__main__":
    main()
