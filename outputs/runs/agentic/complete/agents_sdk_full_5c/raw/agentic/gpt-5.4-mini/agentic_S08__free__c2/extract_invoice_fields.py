from __future__ import annotations

"""Invoice field extraction using Google Cloud Document AI."""

import os
from typing import Any, List

from document_client import get_google_documentai_client
from document_models import ExtractionRequest, ExtractionResponse, FieldValue, normalize_confidence

GOOGLE_DOCUMENT_AI_PROCESSOR_ID = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", "")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
GOOGLE_DOCUMENT_AI_PROCESSOR_VERSION = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_VERSION", "latest")


def _entity_to_field(entity: Any) -> FieldValue:
    mention = getattr(entity, "mention_text", "") or getattr(entity, "normalized_value", None)
    value = str(mention) if mention is not None else ""
    return FieldValue(
        name=getattr(entity, "type_", "unknown"),
        value=value,
        confidence=normalize_confidence(getattr(entity, "confidence", None)),
        raw={"type": getattr(entity, "type_", None), "value": value},
    )


def extract_invoice_fields(request: ExtractionRequest) -> ExtractionResponse:
    client = get_google_documentai_client()
    name = client.processor_path(GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, GOOGLE_DOCUMENT_AI_PROCESSOR_ID)
    document = client.process_document(
        request={"name": name, "raw_document": request.to_google_raw_document(), "skip_human_review": True}
    ).document

    fields: List[FieldValue] = []
    for entity in getattr(document, "entities", []):
        entity_type = getattr(entity, "type_", "")
        if entity_type in {"supplier_name", "invoice_date", "total_amount", "line_item"}:
            fields.append(_entity_to_field(entity))

    if not fields:
        fields = [FieldValue(name="invoice_fields", value="", confidence=0.0, raw={"provider": "google_document_ai"})]

    return ExtractionResponse(
        document_type="invoice",
        provider="google_document_ai",
        model_id=f"projects/{GOOGLE_CLOUD_PROJECT}/locations/{GOOGLE_CLOUD_LOCATION}/processors/{GOOGLE_DOCUMENT_AI_PROCESSOR_ID}/{GOOGLE_DOCUMENT_AI_PROCESSOR_VERSION}",
        fields=fields,
        metadata={"source": request.source_name, "page_count": request.page_count},
    )
