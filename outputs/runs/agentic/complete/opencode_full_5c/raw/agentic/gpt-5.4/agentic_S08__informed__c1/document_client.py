from __future__ import annotations

import os
from typing import Any

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def begin_invoice_analysis(
    document_bytes: bytes, content_type: str = "application/pdf"
) -> Any:
    client = get_document_intelligence_client()
    return client.begin_analyze_document(
        model_id="prebuilt-invoice",
        body=document_bytes,
        content_type=content_type,
    )


def get_field_content(field: Any) -> Any:
    if field is None:
        return None
    for attr in (
        "value_string",
        "value_date",
        "value_currency",
        "value_number",
        "value_integer",
    ):
        if hasattr(field, attr):
            value = getattr(field, attr)
            if value is not None:
                if attr == "value_currency" and hasattr(value, "amount"):
                    return value.amount
                return value
    return getattr(field, "content", None)


def get_field_confidence(field: Any) -> float | None:
    return getattr(field, "confidence", None) if field is not None else None


def field_to_pair(field: Any) -> tuple[Any, float | None]:
    return get_field_content(field), get_field_confidence(field)
