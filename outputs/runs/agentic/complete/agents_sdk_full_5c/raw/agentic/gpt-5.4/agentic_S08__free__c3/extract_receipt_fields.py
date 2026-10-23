from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import (
    AZURE_FORM_RECOGNIZER_MODEL_RECEIPT,
    AzureDocumentIntelligenceClient,
    get_field_confidence,
    get_field_value,
    get_first_document,
)
from document_models import ExtractedDocument, LineItem, document_to_dict, to_float


PROVIDER = "azure-document-intelligence"
MODEL_ID = AZURE_FORM_RECOGNIZER_MODEL_RECEIPT


class ReceiptFieldExtractor:
    def __init__(self, client: Optional[AzureDocumentIntelligenceClient] = None):
        self.client = client or AzureDocumentIntelligenceClient()

    def extract_from_url(self, document_url: str) -> Dict[str, Any]:
        result = self.client.analyze_document_url(MODEL_ID, document_url)
        return self._parse_result(result)

    def extract_from_bytes(self, content: bytes, content_type: str = "image/jpeg") -> Dict[str, Any]:
        result = self.client.analyze_document_bytes(MODEL_ID, content, content_type=content_type)
        return self._parse_result(result)

    def _parse_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        doc = get_first_document(result)
        fields = doc.get("fields", {})
        items: List[LineItem] = []
        item_field = fields.get("Items") or {}
        for entry in get_field_value(item_field) or []:
            value_object = entry.get("valueObject", {})
            total_price = get_field_value(value_object.get("TotalPrice") or {})
            if isinstance(total_price, dict):
                total_price = total_price.get("amount")
            items.append(
                LineItem(
                    description=str(get_field_value(value_object.get("Description") or {}) or ""),
                    quantity=to_float(get_field_value(value_object.get("Quantity") or {})),
                    unit_price=to_float(get_field_value(value_object.get("Price") or {})),
                    amount=to_float(total_price),
                    confidence=get_field_confidence(entry),
                )
            )

        total_value = get_field_value(fields.get("Total") or {})
        tax_value = get_field_value(fields.get("TotalTax") or {})
        currency = None
        if isinstance(total_value, dict):
            currency = total_value.get("currencyCode")
            total_value = total_value.get("amount")
        if isinstance(tax_value, dict):
            tax_value = tax_value.get("amount")

        extracted = ExtractedDocument(
            document_type="receipt",
            merchant=str(get_field_value(fields.get("MerchantName") or {}) or "") or None,
            invoice_date=str(get_field_value(fields.get("TransactionDate") or {}) or "") or None,
            tax=to_float(tax_value),
            total=to_float(total_value),
            currency=currency,
            line_items=items,
            raw_fields=fields,
            provider=PROVIDER,
            model=MODEL_ID,
        )
        return document_to_dict(extracted)
