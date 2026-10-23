from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_client import build_document_intelligence_client
from document_models import StructuredDocumentResponse, StructuredDocumentField


MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(document_bytes: bytes, content_type: str = "application/pdf") -> StructuredDocumentResponse:
    client: DocumentIntelligenceClient = build_document_intelligence_client()
    poller = client.begin_analyze_document(MODEL_ID, document=document_bytes, content_type=content_type)
    result = poller.result()
    fields = []
    invoice = getattr(result, "documents", [None])[0]
    if invoice and getattr(invoice, "fields", None):
        for name in ("VendorName", "InvoiceDate", "InvoiceTotal", "Items"):
            item = invoice.fields.get(name)
            if item is not None:
                fields.append(
                    StructuredDocumentField(
                        name=name,
                        value=getattr(item, "value", None),
                        confidence=float(getattr(item, "confidence", 0.0) or 0.0),
                    )
                )
    raw: Dict[str, Any] = {"provider": "azure-document-intelligence", "model_id": MODEL_ID}
    return StructuredDocumentResponse(provider="azure-document-intelligence", model_id=MODEL_ID, fields=fields, raw_response=raw)
