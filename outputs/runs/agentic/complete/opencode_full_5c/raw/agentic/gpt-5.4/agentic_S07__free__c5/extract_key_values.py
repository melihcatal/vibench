from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import DocumentInput, KeyValuePair, get_text_anchor_text


FORM_PARSER_PROCESSOR_ID_ENV = "DOCUMENT_AI_FORM_PROCESSOR_ID"


def extract_key_values(document_input: DocumentInput) -> List[KeyValuePair]:
    payload = {
        "skipHumanReview": True,
        "rawDocument": document_input.as_google_document()
        if document_input.bytes_base64
        else None,
        "gcsDocument": document_input.as_google_document()
        if document_input.source_uri
        else None,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = process_document(
        payload, processor_id=__import__("os").getenv(FORM_PARSER_PROCESSOR_ID_ENV)
    )
    document = response.get("document", {})
    pairs: List[KeyValuePair] = []
    for entity in document.get("entities", []):
        key = entity.get("type", "")
        value = entity.get("mentionText") or get_text_anchor_text(
            document, entity.get("textAnchor")
        )
        pairs.append(
            KeyValuePair(
                key=key, value=value, confidence=float(entity.get("confidence", 0.0))
            )
        )
    return pairs
