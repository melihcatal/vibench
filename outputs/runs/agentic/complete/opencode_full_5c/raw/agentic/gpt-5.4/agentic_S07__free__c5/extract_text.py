from __future__ import annotations

from typing import Any, Dict, List

from document_client import process_document
from document_models import (
    DocumentInput,
    OCRTextResult,
    NormalizedTextBlock,
    get_text_anchor_text,
    normalize_bbox,
)


def extract_text(document_input: DocumentInput) -> OCRTextResult:
    payload = {
        "skipHumanReview": True,
        "rawDocument": document_input.as_google_document()
        if document_input.bytes_base64
        else None,
        "gcsDocument": document_input.as_google_document()
        if document_input.source_uri
        else None,
        "processOptions": {
            "ocrConfig": {
                "enableNativePdfParsing": True,
                "enableImageQualityScores": True,
            }
        },
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = process_document(payload)
    document = response.get("document", {})
    pages = document.get("pages", [])
    blocks: List[NormalizedTextBlock] = []
    for page_index, page in enumerate(pages, start=1):
        for block in page.get("blocks", []):
            layout = block.get("layout", {})
            blocks.append(
                NormalizedTextBlock(
                    text=get_text_anchor_text(document, layout.get("textAnchor")),
                    page=page_index,
                    block_type="block",
                    bbox=normalize_bbox(layout.get("boundingPoly", {}).get("vertices")),
                )
            )
    return OCRTextResult(text=document.get("text", ""), pages=len(pages), blocks=blocks)
