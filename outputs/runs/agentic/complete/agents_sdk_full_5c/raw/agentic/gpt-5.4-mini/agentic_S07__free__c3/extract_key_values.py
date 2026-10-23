from __future__ import annotations

from typing import List

from google.cloud import documentai

from document_client import DocumentAiConfig, build_document_ai_client, build_process_request
from document_models import KeyValuePair, KeyValueResponse, normalize_document_ai_text


def extract_key_values(image_bytes: bytes, mime_type: str = "image/png") -> KeyValueResponse:
    config = DocumentAiConfig()
    client = build_document_ai_client(config.endpoint)
    request = build_process_request(image_bytes, mime_type=mime_type, config=config)
    response = client.process_document(request=request)
    document = response.document
    pairs: List[KeyValuePair] = []
    for page in document.pages:
        for kv in getattr(page, "form_fields", []):
            key = normalize_document_ai_text(documentai.Document.TextAnchor.get_text(kv.field_name.text_anchor, document.text))
            value = normalize_document_ai_text(documentai.Document.TextAnchor.get_text(kv.field_value.text_anchor, document.text))
            pairs.append(KeyValuePair(key=key, value=value, confidence=float(kv.field_name.confidence or 0.0)))
    return KeyValueResponse(pairs=pairs, raw={"provider": "google_document_ai"})
