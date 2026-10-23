import os
from typing import Dict, Any
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from document_client import get_document_intelligence_client
from document_models import InvoiceExtractionResponse


def extract_invoice_fields(file_path: str, mime_type: str) -> InvoiceExtractionResponse:
    client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_type=mime_type,
            output_content_format=ContentFormat.MARKDOWN
        )

    result = poller.result()

    fields = {}
    if result.documents:
        document = result.documents[0]
        fields["vendor"] = document.fields.get("VendorName", {}).get("content", "")
        fields["date"] = document.fields.get("InvoiceDate", {}).get("content", "")
        fields["total"] = document.fields.get("InvoiceTotal", {}).get("content", "")
        fields["line_items"] = []
        if document.fields.get("Items"):
            for item in document.fields["Items"].get("valueArray", []):
                line_item = {
                    "description": item.get("valueObject", {}).get("Description", {}).get("content", ""),
                    "amount": item.get("valueObject", {}).get("Amount", {}).get("content", ""),
                    "quantity": item.get("valueObject", {}).get("Quantity", {}).get("content", "")
                }
                fields["line_items"].append(line_item)

    return InvoiceExtractionResponse(
        raw_fields=fields,
        confidence=result.confidence,
        model_used="prebuilt-invoice"
    )