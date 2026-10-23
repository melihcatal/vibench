from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import (
    AZURE_FORM_RECOGNIZER_MODEL_INVOICE,
    AzureDocumentIntelligenceClient,
    get_field_confidence,
    get_field_value,
    get_first_document,
)
from document_models import ExtractedDocument, LineItem, document_to_dict, to_float


PROVIDER = "azure-document-intelligence"
MODEL_ID = AZURE_FORM_RECOGNIZER_MODEL_INVOICE


class InvoiceFieldExtractor:
    def __init__(self, client: Optional[AzureDocumentIntelligenceClient] = None):
        self.client = client or AzureDocumentIntelligenceClient()

    def extract_from_url(self, document_url: str) -> Dict[str, Any]:
        result = self.client.analyze_document_url(MODEL_ID, document_url)
        return self._parse_result(result)

    def extract_from_bytes(self, content: bytes, content_type: str = "application/pdf") -> Dict[str, Any]:
        result = self.client.analyze_document_bytes(MODEL_ID, content, content_type=content_type)
        return self._parse_result(result)

    def _parse_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        doc = get_first_document(result)
        fields = doc.get("fields", {})
        items: List[LineItem] = []
        item_field = fields.get("Items") or {}
        for entry in get_field_value(item_field) or []:
            value_object = entry.get("valueObject", {})
            amount_field = value_object.get("Amount") or {}
            quantity_field = value_object.get("Quantity") or {}
            unit_price_field = value_object.get("UnitPrice") or {}
            description_field = value_object.get("Description") or {}
            amount_value = get_field_value(amount_field)
            if isinstance(amount_value, dict):
                amount_value = amount_value.get("amount")
            unit_price_value = get_field_value(unit_price_field)
            if isinstance(unit_price_value, dict):
                unit_price_value = unit_price_value.get("amount")
            items.append(
                LineItem(
                    description=str(get_field_value(description_field) or ""),
                    quantity=to_float(get_field_value(quantity_field)),
                    unit_price=to_float(unit_price_value),
                    amount=to_float(amount_value),
                    confidence=get_field_confidence(entry),
                )
            )

        total_value = get_field_value(fields.get("InvoiceTotal") or {})
        if isinstance(total_value, dict):
            total_amount = total_value.get("amount")
            currency = total_value.get("currencyCode")
        else:
            total_amount = total_value
            currency = None

        extracted = ExtractedDocument(
            document_type="invoice",
            vendor=str(get_field_value(fields.get("VendorName") or {}) or "") or None,
            invoice_date=str(get_field_value(fields.get("InvoiceDate") or {}) or "") or None,
            total=to_float(total_amount),
            currency=currency,
            notes=str(get_field_value(fields.get("CustomerName") or {}) or "") or None,
            line_items=items,
            raw_fields=fields,
            provider=PROVIDER,
            model=MODEL_ID,
        )
        return document_to_dict(extracted)
