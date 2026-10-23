from __future__ import annotations

from typing import List

from document_client import process_document_bytes
from document_models import KeyValuePair, get_text_from_anchor


DEFAULT_MIME_TYPE = "image/png"


def extract_key_values(file_path: str, mime_type: str = DEFAULT_MIME_TYPE) -> List[KeyValuePair]:
    with open(file_path, "rb") as f:
        result = process_document_bytes(f.read(), mime_type)
    document = result.document
    pairs: List[KeyValuePair] = []
    for page in document.pages:
        for form_field in page.form_fields:
            key_text = get_text_from_anchor(document, form_field.field_name.text_anchor)
            value_text = get_text_from_anchor(document, form_field.field_value.text_anchor)
            pairs.append(
                KeyValuePair(
                    key=key_text,
                    value=value_text,
                    confidence=min(
                        float(getattr(form_field.field_name, "confidence", 0.0) or 0.0),
                        float(getattr(form_field.field_value, "confidence", 0.0) or 0.0),
                    ),
                    page=page.page_number,
                )
            )
    return pairs
