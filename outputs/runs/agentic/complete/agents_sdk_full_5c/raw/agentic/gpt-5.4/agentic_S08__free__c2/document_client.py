from __future__ import annotations

import base64
import os
from typing import Any, Dict

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import DocumentExtractionResult, ExtractedField, LineItem


class AzureDocumentExtractionClient:
    def __init__(self, endpoint: str | None = None, api_key: str | None = None) -> None:
        self.endpoint = endpoint or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.api_key = api_key or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        if not self.endpoint or not self.api_key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
        )

    def analyze_invoice(self, document_bytes: bytes) -> DocumentExtractionResult:
        poller = self.client.begin_analyze_document(
            model_id="prebuilt-invoice",
            body={"base64Source": base64.b64encode(document_bytes).decode("utf-8")},
        )
        result = poller.result()
        doc = result.documents[0] if result.documents else None
        fields = doc.fields if doc else {}
        line_items = []
        items_field = fields.get("Items") if fields else None
        if items_field and getattr(items_field, "value_array", None):
            for entry in items_field.value_array:
                obj = entry.value_object or {}
                line_items.append(
                    LineItem(
                        description=_field_content(obj.get("Description")),
                        quantity=_field_number(obj.get("Quantity")),
                        unit_price=_field_number(obj.get("UnitPrice")),
                        amount=_field_number(obj.get("Amount")),
                        confidence=getattr(entry, "confidence", None),
                    )
                )
        return DocumentExtractionResult(
            document_type="invoice",
            vendor=_wrapped_field(fields.get("VendorName")),
            date=_wrapped_field(fields.get("InvoiceDate")),
            total=_wrapped_field(fields.get("InvoiceTotal")),
            currency=_wrapped_field(fields.get("CurrencyCode")),
            line_items=line_items,
            raw_response=result.as_dict(),
        )

    def analyze_receipt(self, document_bytes: bytes) -> DocumentExtractionResult:
        poller = self.client.begin_analyze_document(
            model_id="prebuilt-receipt",
            body={"base64Source": base64.b64encode(document_bytes).decode("utf-8")},
        )
        result = poller.result()
        doc = result.documents[0] if result.documents else None
        fields = doc.fields if doc else {}
        line_items = []
        items_field = fields.get("Items") if fields else None
        if items_field and getattr(items_field, "value_array", None):
            for entry in items_field.value_array:
                obj = entry.value_object or {}
                line_items.append(
                    LineItem(
                        description=_field_content(obj.get("Description")),
                        quantity=_field_number(obj.get("Quantity")),
                        unit_price=_field_number(obj.get("Price")),
                        amount=_field_number(obj.get("TotalPrice")),
                        confidence=getattr(entry, "confidence", None),
                    )
                )
        return DocumentExtractionResult(
            document_type="receipt",
            merchant=_wrapped_field(fields.get("MerchantName")),
            date=_wrapped_field(fields.get("TransactionDate")),
            tax=_wrapped_field(fields.get("TotalTax")),
            total=_wrapped_field(fields.get("Total")),
            currency=_wrapped_field(fields.get("CurrencyCode")),
            line_items=line_items,
            raw_response=result.as_dict(),
        )


def _wrapped_field(field: Any) -> ExtractedField | None:
    if not field:
        return None
    return ExtractedField(
        value=_field_content(field),
        confidence=getattr(field, "confidence", None),
        source="azure-document-intelligence",
    )


def _field_content(field: Any) -> Any:
    if not field:
        return None
    for attr in ("value_string", "value_currency", "value_date", "content", "value_number"):
        value = getattr(field, attr, None)
        if value is not None:
            if attr == "value_currency":
                amount = getattr(value, "amount", None)
                if amount is not None:
                    return amount
            return str(value) if attr == "value_date" else value
    return getattr(field, "content", None)


def _field_number(field: Any) -> float | None:
    value = _field_content(field)
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def extraction_result_to_dict(result: DocumentExtractionResult) -> Dict[str, Any]:
    return result.to_dict()
