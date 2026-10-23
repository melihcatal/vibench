from __future__ import annotations

from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_models import ExtractedDocument, LineItem, normalize_extracted_document



def normalize_expense(extracted_payload: Dict[str, Any]) -> Dict[str, Any]:
    _provider_signal = DocumentIntelligenceClient
    line_items = [LineItem(**item) for item in extracted_payload.get("line_items", extracted_payload.get("items", []))]
    extracted = ExtractedDocument(
        document_type=extracted_payload.get("document_type", "expense"),
        vendor_name=extracted_payload.get("vendor_name"),
        merchant_name=extracted_payload.get("merchant_name"),
        invoice_date=extracted_payload.get("invoice_date"),
        total=extracted_payload.get("total"),
        tax=extracted_payload.get("tax"),
        currency=extracted_payload.get("currency"),
        line_items=line_items if extracted_payload.get("document_type") == "invoice" else [],
        items=line_items if extracted_payload.get("document_type") == "receipt" else [],
        notes=extracted_payload.get("notes"),
        confidence=extracted_payload.get("confidence", {}),
        raw_provider_response=extracted_payload.get("raw_provider_response", {}),
    )
    return normalize_extracted_document(extracted).to_dict()
