import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

from document_models import (
    DocumentExtractionRequest,
    ExtractedField,
    InvoiceExtraction,
    LineItem,
    ReceiptExtraction,
    ReceiptItem,
)


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

PREBUILT_INVOICE_MODEL_ID = "prebuilt-invoice"
PREBUILT_RECEIPT_MODEL_ID = "prebuilt-receipt"


class DocumentClient:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        key: Optional[str] = None,
    ):
        self.endpoint = endpoint or AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
        self.key = key or AZURE_DOCUMENT_INTELLIGENCE_KEY
        self._client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key),
        )

    def analyze_document(
        self, model_id: str, request: DocumentExtractionRequest
    ) -> dict:
        if request.file_bytes:
            poller = self._client.begin_analyze_document(
                model_id=model_id,
                analyze_request=AnalyzeDocumentRequest(bytes_source=request.file_bytes),
                content_type=request.content_type,
            )
        elif request.file_path:
            with open(request.file_path, "rb") as f:
                file_bytes = f.read()
            poller = self._client.begin_analyze_document(
                model_id=model_id,
                analyze_request=AnalyzeDocumentRequest(bytes_source=file_bytes),
                content_type=request.content_type,
            )
        else:
            raise ValueError("Either file_path or file_bytes must be provided")
        result = poller.result()
        return result.to_dict()

    @staticmethod
    def _get_field_value(fields: dict, field_name: str) -> ExtractedField:
        field_data = fields.get(field_name)
        if field_data is None:
            return ExtractedField(value="")
        return ExtractedField(
            value=field_data.get("value", ""),
            confidence=field_data.get("confidence", 0.0),
        )

    @staticmethod
    def _get_field_float(fields: dict, field_name: str) -> ExtractedField:
        field_data = fields.get(field_name)
        if field_data is None:
            return ExtractedField(value=0.0)
        raw_value = field_data.get("value", 0.0)
        try:
            numeric_value = float(raw_value)
        except (TypeError, ValueError):
            numeric_value = 0.0
        return ExtractedField(
            value=numeric_value,
            confidence=field_data.get("confidence", 0.0),
        )

    def parse_invoice(self, request: DocumentExtractionRequest) -> InvoiceExtraction:
        raw = self.analyze_document(PREBUILT_INVOICE_MODEL_ID, request)
        documents = raw.get("documents", [])
        if not documents:
            return InvoiceExtraction(raw_response=raw)
        doc = documents[0]
        fields = doc.get("fields", {})
        vendor = self._get_field_value(fields, "VendorName")
        invoice_date = self._get_field_value(fields, "InvoiceDate")
        invoice_total = self._get_field_float(fields, "InvoiceTotal")
        line_items = []
        items_field = fields.get("Items", {})
        items_value = items_field.get("value", [])
        if isinstance(items_value, list):
            for item in items_value:
                item_fields = item.get("value", {}) if isinstance(item, dict) else {}
                line_items.append(
                    LineItem(
                        description=self._get_field_value(item_fields, "Description"),
                        quantity=self._get_field_value(item_fields, "Quantity"),
                        unit_price=self._get_field_float(item_fields, "UnitPrice"),
                        total_price=self._get_field_float(item_fields, "Amount"),
                    )
                )
        return InvoiceExtraction(
            vendor_name=vendor,
            invoice_date=invoice_date,
            invoice_total=invoice_total,
            line_items=line_items,
            raw_response=raw,
        )

    def parse_receipt(self, request: DocumentExtractionRequest) -> ReceiptExtraction:
        raw = self.analyze_document(PREBUILT_RECEIPT_MODEL_ID, request)
        documents = raw.get("documents", [])
        if not documents:
            return ReceiptExtraction(raw_response=raw)
        doc = documents[0]
        fields = doc.get("fields", {})
        merchant = self._get_field_value(fields, "MerchantName")
        tax = self._get_field_float(fields, "TotalTax")
        total = self._get_field_float(fields, "Total")
        items = []
        items_field = fields.get("Items", {})
        items_value = items_field.get("value", [])
        if isinstance(items_value, list):
            for item in items_value:
                item_fields = item.get("value", {}) if isinstance(item, dict) else {}
                items.append(
                    ReceiptItem(
                        description=self._get_field_value(item_fields, "Description"),
                        price=self._get_field_float(item_fields, "TotalPrice"),
                    )
                )
        return ReceiptExtraction(
            merchant_name=merchant,
            tax_amount=tax,
            receipt_total=total,
            items=items,
            raw_response=raw,
        )
