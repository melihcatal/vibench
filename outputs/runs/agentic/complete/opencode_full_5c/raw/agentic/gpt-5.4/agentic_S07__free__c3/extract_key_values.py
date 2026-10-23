from __future__ import annotations

from document_client import (
    GOOGLE_VISION_API_URL,
    build_google_query_params,
    build_google_vision_headers,
    build_vision_requests,
    extract_full_text_annotation,
    post_json,
)
from document_models import DocumentSource, KeyValueResult, compact_whitespace


def extract_key_values(document: DocumentSource) -> KeyValueResult:
    payload = build_vision_requests(document, [{"type": "DOCUMENT_TEXT_DETECTION"}])
    response_json = post_json(
        GOOGLE_VISION_API_URL,
        payload,
        headers=build_google_vision_headers(),
        params=build_google_query_params("GOOGLE_CLOUD_API_KEY"),
    )
    annotation = extract_full_text_annotation(response_json)
    pairs = []
    for page in annotation.get("pages", []):
        for block in page.get("blocks", []):
            for paragraph in block.get("paragraphs", []):
                line = compact_whitespace(
                    " ".join(
                        "".join(
                            symbol.get("text", "") for symbol in word.get("symbols", [])
                        )
                        for word in paragraph.get("words", [])
                    )
                )
                if not line:
                    continue
                if ":" in line:
                    key, value = line.split(":", 1)
                elif "-" in line:
                    key, value = line.split("-", 1)
                else:
                    continue
                key = compact_whitespace(key)
                value = compact_whitespace(value)
                if key and value:
                    pairs.append({"key": key, "value": value})
    return KeyValueResult(
        provider="google-cloud-vision", pairs=pairs, raw_response=response_json
    )
