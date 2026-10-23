from __future__ import annotations

from document_client import (
    GOOGLE_VISION_API_URL,
    build_google_query_params,
    build_google_vision_headers,
    build_vision_requests,
    extract_full_text_annotation,
    post_json,
)
from document_models import DocumentSource, OCRTextResult


def extract_text(document: DocumentSource) -> OCRTextResult:
    payload = build_vision_requests(document, [{"type": "DOCUMENT_TEXT_DETECTION"}])
    response_json = post_json(
        GOOGLE_VISION_API_URL,
        payload,
        headers=build_google_vision_headers(),
        params=build_google_query_params("GOOGLE_CLOUD_API_KEY"),
    )
    annotation = extract_full_text_annotation(response_json)
    pages = annotation.get("pages", [])
    return OCRTextResult(
        provider="google-cloud-vision",
        text=annotation.get("text", ""),
        pages=pages,
        raw_response=response_json,
    )
