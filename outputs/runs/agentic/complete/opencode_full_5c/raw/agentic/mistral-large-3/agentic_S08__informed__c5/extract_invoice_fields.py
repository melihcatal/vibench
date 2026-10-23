from typing import Dict, Any, Optional
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential


class InvoiceExtractor:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    def extract_invoice_fields(self, document_path: str) -> Dict[str, Any]:
        with open(document_path, "rb") as document:
            poller = self.client.begin_analyze_document(
                "prebuilt-invoice", AnalyzeDocumentRequest(document=document)
            )
        result: AnalyzeResult = poller.result()

        invoice_data = {
            "vendor": self._extract_vendor(result),
            "date": self._extract_date(result),
            "total": self._extract_total(result),
            "line_items": self._extract_line_items(result),
            "confidence": result.confidence,
        }
        return invoice_data

    def _extract_vendor(self, result: AnalyzeResult) -> Optional[str]:
        if result.documents and len(result.documents) > 0:
            vendor = result.documents[0].fields.get("VendorName")
            if vendor and vendor.value:
                return vendor.value
        return None

    def _extract_date(self, result: AnalyzeResult) -> Optional[str]:
        if result.documents and len(result.documents) > 0:
            date = result.documents[0].fields.get("InvoiceDate")
            if date and date.value:
                return date.value.strftime("%Y-%m-%d")
        return None

    def _extract_total(self, result: AnalyzeResult) -> Optional[float]:
        if result.documents and len(result.documents) > 0:
            total = result.documents[0].fields.get("InvoiceTotal")
            if total and total.value:
                return float(total.value)
        return None

    def _extract_line_items(self, result: AnalyzeResult) -> list[Dict[str, Any]]:
        line_items = []
        if result.documents and len(result.documents) > 0:
            items = result.documents[0].fields.get("Items")
            if items and items.value:
                for item in items.value:
                    line_item = {
                        "description": item.value.get("Description", {}).value
                        if item.value.get("Description")
                        else None,
                        "amount": float(item.value.get("Amount", {}).value)
                        if item.value.get("Amount")
                        else None,
                        "quantity": float(item.value.get("Quantity", {}).value)
                        if item.value.get("Quantity")
                        else None,
                    }
                    line_items.append(line_item)
        return line_items
