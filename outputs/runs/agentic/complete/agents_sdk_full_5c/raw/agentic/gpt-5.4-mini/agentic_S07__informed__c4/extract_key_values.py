from __future__ import annotations

from typing import List

from document_client import DocumentAIClientHelper
from document_models import DocumentRequest, KeyValuePair, normalize_text


def extract_key_values(file_path: str, mime_type: str = "image/png") -> List[KeyValuePair]:
    helper = DocumentAIClientHelper()
    response = helper.process(DocumentRequest(file_path=file_path, mime_type=mime_type))
    document = response.document
    pairs: List[KeyValuePair] = []
    for page in getattr(document, "pages", []):
        for kv in getattr(page, "form_fields", []):
            key = normalize_text(getattr(getattr(kv, "field_name", None), "text_anchor", {}))
            value = normalize_text(getattr(getattr(kv, "field_value", None), "text_anchor", {}))
            pairs.append(KeyValuePair(key=key, value=value, raw=kv))
    return pairs
