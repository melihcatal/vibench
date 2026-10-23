from __future__ import annotations

from document_client import (
    GOOGLE_VISION_API_URL,
    build_google_query_params,
    build_google_vision_headers,
    build_vision_requests,
    extract_full_text_annotation,
    post_json,
)
from document_models import (
    DocumentSource,
    TableResult,
    compact_whitespace,
    normalize_polygon,
)


def extract_tables(document: DocumentSource) -> TableResult:
    payload = build_vision_requests(document, [{"type": "DOCUMENT_TEXT_DETECTION"}])
    response_json = post_json(
        GOOGLE_VISION_API_URL,
        payload,
        headers=build_google_vision_headers(),
        params=build_google_query_params("GOOGLE_CLOUD_API_KEY"),
    )
    annotation = extract_full_text_annotation(response_json)
    tables = []
    for page_index, page in enumerate(annotation.get("pages", [])):
        for block in page.get("blocks", []):
            if block.get("blockType") != "TABLE":
                continue
            rows = []
            for paragraph in block.get("paragraphs", []):
                row_cells = []
                for word in paragraph.get("words", []):
                    cell_text = compact_whitespace(
                        "".join(
                            symbol.get("text", "") for symbol in word.get("symbols", [])
                        )
                    )
                    if cell_text:
                        row_cells.append(
                            {
                                "text": cell_text,
                                "bounding_polygon": normalize_polygon(
                                    word.get("boundingBox", {})
                                ),
                                "confidence": word.get("confidence"),
                            }
                        )
                if row_cells:
                    rows.append({"cells": row_cells})
            tables.append(
                {
                    "page": page_index + 1,
                    "bounding_polygon": normalize_polygon(block.get("boundingBox", {})),
                    "rows": rows,
                }
            )
    return TableResult(
        provider="google-cloud-vision", tables=tables, raw_response=response_json
    )
