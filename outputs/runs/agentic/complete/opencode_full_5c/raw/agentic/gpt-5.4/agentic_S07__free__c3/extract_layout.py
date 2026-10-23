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
    LayoutResult,
    normalize_polygon,
    normalize_text_anchor,
)


def extract_layout(document: DocumentSource) -> LayoutResult:
    payload = build_vision_requests(document, [{"type": "DOCUMENT_TEXT_DETECTION"}])
    response_json = post_json(
        GOOGLE_VISION_API_URL,
        payload,
        headers=build_google_vision_headers(),
        params=build_google_query_params("GOOGLE_CLOUD_API_KEY"),
    )
    annotation = extract_full_text_annotation(response_json)
    full_text = annotation.get("text", "")
    elements = []
    for page_index, page in enumerate(annotation.get("pages", [])):
        for block_index, block in enumerate(page.get("blocks", [])):
            block_text = ""
            lines = []
            for paragraph in block.get("paragraphs", []):
                words = []
                for word in paragraph.get("words", []):
                    token = "".join(
                        symbol.get("text", "") for symbol in word.get("symbols", [])
                    )
                    if token:
                        words.append(token)
                line_text = " ".join(words).strip()
                if line_text:
                    lines.append(line_text)
            block_text = "\n".join(lines).strip() or normalize_text_anchor(
                block.get("layout", {}).get("textAnchor", {}), full_text
            )
            elements.append(
                {
                    "page": page_index + 1,
                    "block_index": block_index,
                    "type": block.get("blockType", "BLOCK"),
                    "text": block_text,
                    "bounding_polygon": normalize_polygon(block.get("boundingBox", {})),
                    "confidence": block.get("confidence"),
                    "lines": lines,
                }
            )
    return LayoutResult(
        provider="google-cloud-vision", elements=elements, raw_response=response_json
    )
