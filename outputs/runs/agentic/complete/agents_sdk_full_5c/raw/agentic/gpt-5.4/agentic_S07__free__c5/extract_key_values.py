from __future__ import annotations

from typing import List

from document_client import process_document
from document_models import KeyValueItem, KeyValueResult, text_anchor_to_string


PROVIDER = "google-document-ai"


def extract_key_values(source: str, mime_type: str | None = None) -> KeyValueResult:
    document = process_document(source=source, mime_type=mime_type)
    items: List[KeyValueItem] = []
    for entity in getattr(document, "entities", []):
        key = getattr(entity, "type_", "")
        value = getattr(entity, "mention_text", "") or text_anchor_to_string(document, getattr(entity, "text_anchor", None))
        confidence = getattr(entity, "confidence", None)
        if key or value:
            items.append(KeyValueItem(key=key, value=value, confidence=confidence))
        for prop in getattr(entity, "properties", []):
            prop_key = getattr(prop, "type_", "")
            prop_value = getattr(prop, "mention_text", "") or text_anchor_to_string(document, getattr(prop, "text_anchor", None))
            items.append(KeyValueItem(key=prop_key, value=prop_value, confidence=getattr(prop, "confidence", None)))
    return KeyValueResult(items=items, raw={"service": "Document AI Form Parser"})
