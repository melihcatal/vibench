from __future__ import annotations

from typing import List

from document_client import document_to_dict, process_document, text_from_layout
from document_models import DocumentRequest, KeyValueItem, KeyValueResult


def extract_key_values(request: DocumentRequest) -> KeyValueResult:
    document = process_document(request, "GOOGLE_DOCUMENTAI_FORM_PARSER_PROCESSOR_ID")
    items: List[KeyValueItem] = []
    for page in document.pages:
        for field in page.form_fields:
            items.append(
                KeyValueItem(
                    key=text_from_layout(document, field.field_name),
                    value=text_from_layout(document, field.field_value),
                    confidence=float(
                        field.field_name.confidence
                        or field.field_value.confidence
                        or 0.0
                    ),
                )
            )
    return KeyValueResult(items=items, provider_payload=document_to_dict(document))
