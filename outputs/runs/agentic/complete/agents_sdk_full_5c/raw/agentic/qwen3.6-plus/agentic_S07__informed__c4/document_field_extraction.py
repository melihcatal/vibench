"""
[LATER-STEP] Extract structured fields from OCR-normalized document text.

Provider: Azure AI Document Intelligence - Prebuilt Invoice processor
SDK: azure-ai-documentintelligence
Auth: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
Service endpoint: cognitiveservices.azure.com
Model: prebuilt-invoice (prebuiltInvoice)
"""

from __future__ import annotations

import os
from typing import Optional, List, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

from document_client import (
    load_image_bytes,
    get_azure_document_intelligence_endpoint,
    get_azure_document_intelligence_key,
)
from document_models import StructuredField


def extract_structured_fields(
    file_path: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    model_id: str = "prebuilt-invoice",
) -> List[StructuredField]:
    """
    Extract structured fields (invoice fields, line items, etc.) from a
    document image or PDF using Azure AI Document Intelligence
    prebuilt-invoice model (prebuiltInvoice) via cognitiveservices.azure.com.

    Uses the azure-ai-documentintelligence SDK.
    """
    endpoint = endpoint or get_azure_document_intelligence_endpoint()
    api_key = api_key or get_azure_document_intelligence_key()

    if not endpoint:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT environment variable or endpoint argument is required"
        )
    if not api_key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_KEY environment variable or api_key argument is required"
        )

    credential = AzureKeyCredential(api_key)
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)

    raw_bytes = load_image_bytes(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    content_type = "application/pdf" if ext == ".pdf" else "image/png"

    poller = client.begin_analyze_document(
        model_id=model_id,
        body=raw_bytes,
        content_type=content_type,
    )

    result: AnalyzeResult = poller.result()
    fields: List[StructuredField] = []

    # Extract top-level invoice fields
    if result.documents:
        for doc in result.documents:
            doc_fields = doc.fields if hasattr(doc, "fields") and doc.fields else {}
            for field_name, field_value in doc_fields.items():
                structured = _parse_invoice_field(field_name, field_value)
                if structured:
                    fields.append(structured)

    return fields


def _parse_invoice_field(
    field_name: str,
    field_value,
) -> Optional[StructuredField]:
    """Parse a single Azure Document Intelligence field into StructuredField."""
    if field_value is None:
        return None

    value_str = ""
    confidence = getattr(field_value, "confidence", 1.0)
    field_type = getattr(field_value, "type", "string")

    if hasattr(field_value, "value"):
        value = field_value.value
        if isinstance(value, (str, int, float)):
            value_str = str(value)
        elif isinstance(value, dict):
            value_str = _dict_to_string(value)
        elif isinstance(value, list):
            # Handle line items or arrays
            value_str = "; ".join(
                str(item) for item in value if item is not None
            )
        elif value is not None:
            value_str = str(value)

    return StructuredField(
        field_name=field_name,
        value=value_str,
        confidence=confidence,
        field_type=field_type,
    )


def _dict_to_string(d: Dict) -> str:
    """Convert a dictionary field value to a string representation."""
    parts = []
    for k, v in d.items():
        if v is not None:
            parts.append(f"{k}: {v}")
    return ", ".join(parts)


def extract_invoice_fields_as_dict(
    file_path: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    model_id: str = "prebuilt-invoice",
) -> Dict[str, str]:
    """
    Extract structured invoice fields as a dictionary using Azure AI
    Document Intelligence prebuilt-invoice model.
    """
    fields = extract_structured_fields(
        file_path=file_path,
        endpoint=endpoint,
        api_key=api_key,
        model_id=model_id,
    )
    return {f.field_name: f.value for f in fields}
