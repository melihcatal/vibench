from typing import Dict, Any, Optional
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential


def extract_invoice_fields(
    file_path: str, mime_type: str = "application/pdf"
) -> Dict[str, Any]:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Azure Document Intelligence.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence endpoint and key must be set in environment variables."
        )

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
        )

    result: AnalyzeResult = poller.result()

    extracted_data = {
        "vendor": None,
        "date": None,
        "total": None,
        "line_items": [],
        "confidence": result.confidence,
    }

    if result.documents:
        invoice = result.documents[0].fields

        if invoice.get("VendorName"):
            extracted_data["vendor"] = invoice["VendorName"].value

        if invoice.get("InvoiceDate"):
            extracted_data["date"] = invoice["InvoiceDate"].value.isoformat()

        if invoice.get("InvoiceTotal"):
            extracted_data["total"] = float(invoice["InvoiceTotal"].value)

        if invoice.get("Items"):
            for item in invoice["Items"].value:
                line_item = {
                    "description": item.value.get("Description", {}).value
                    if item.value.get("Description")
                    else None,
                    "amount": float(item.value["Amount"].value)
                    if item.value.get("Amount")
                    else None,
                    "quantity": float(item.value["Quantity"].value)
                    if item.value.get("Quantity")
                    else None,
                }
                extracted_data["line_items"].append(line_item)

    return extracted_data
