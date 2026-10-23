from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import get_document_analysis_client, load_document_bytes
from document_models import DocumentExtractionResult, ExtractedField, LineItem



def extract_receipt_fields(
    file_path: Optional[str] = None,
    content_base64: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_document_analysis_client()
    payload = load_document_bytes(path=file_path, content_base64=content_base64)
    poller = client.begin_analyze_document("prebuilt-receipt", document=payload)
    result = poller.result()

    if not result.documents:
        return DocumentExtractionResult(document_type="receipt", provider="azure-ai-formrecognizer").to_dict()

    doc = result.documents[0]
    fields = getattr(doc, "fields", {}) or {}

    merchant_field = fields.get("MerchantName")
    total_field = fields.get("Total")
    tax_field = fields.get("TotalTax")
    date_field = fields.get("TransactionDate")

    items: List[LineItem] = []
    items_field = fields.get("Items")
    if items_field and getattr(items_field, "value", None):
        for entry in items_field.value:
            item_map = getattr(entry, "value", {}) or {}
            name = item_map.get("Name")
            price = item_map.get("TotalPrice")
            quantity = item_map.get("Quantity")
            items.append(
                LineItem(
                    description=getattr(name, "content", None) or getattr(name, "value", None) or "",
                    quantity=getattr(quantity, "value", None),
                    total=getattr(price, "value", None),
                    confidence=max(
                        float(getattr(name, "confidence", 0.0) or 0.0),
                        float(getattr(price, "confidence", 0.0) or 0.0),
                    ),
                )
            )

    extracted = DocumentExtractionResult(
        document_type="receipt",
        provider="azure-ai-formrecognizer",
        merchant=ExtractedField(
            value=getattr(merchant_field, "value", None) or getattr(merchant_field, "content", None),
            confidence=float(getattr(merchant_field, "confidence", 0.0) or 0.0),
        ),
        date=ExtractedField(
            value=str(getattr(date_field, "value", None)) if date_field else None,
            confidence=float(getattr(date_field, "confidence", 0.0) or 0.0),
        ),
        tax=ExtractedField(
            value=getattr(tax_field, "value", None) if tax_field else None,
            confidence=float(getattr(tax_field, "confidence", 0.0) or 0.0),
        ),
        total=ExtractedField(
            value=getattr(total_field, "value", None) if total_field else None,
            confidence=float(getattr(total_field, "confidence", 0.0) or 0.0),
        ),
        line_items=items,
        raw_response={"model_id": "prebuilt-receipt", "api_version": getattr(result, "api_version", None)},
    )
    return extracted.to_dict()
