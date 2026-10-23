from __future__ import annotations

from typing import List

from document_client import (
    build_process_request,
    document_to_dict,
    get_documentai_client,
    get_processor_name,
)
from document_models import DocumentInput, KeyValueExtractionResult, KeyValueItem


def extract_key_values(
    document: DocumentInput, processor_id: str | None = None
) -> KeyValueExtractionResult:
    client = get_documentai_client()
    request = build_process_request(
        document, get_processor_name(processor_id=processor_id)
    )
    response = client.process_document(request=request)
    processed = response.document
    items: List[KeyValueItem] = []
    for page_index, page in enumerate(processed.pages, start=1):
        for form_field in page.form_fields:
            items.append(
                KeyValueItem(
                    key=_anchor_text(processed.text, form_field.field_name.text_anchor),
                    value=_anchor_text(
                        processed.text, form_field.field_value.text_anchor
                    ),
                    confidence=getattr(form_field.field_value, "confidence", None),
                    page=page_index,
                )
            )
    return KeyValueExtractionResult(
        provider="google_document_ai",
        items=items,
        raw_response=document_to_dict(processed),
    )


def _anchor_text(full_text: str, anchor) -> str:
    if not getattr(anchor, "text_segments", None):
        return ""
    return "".join(
        full_text[int(getattr(seg, "start_index", 0) or 0) : int(seg.end_index)]
        for seg in anchor.text_segments
    ).strip()
