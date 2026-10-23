from typing import Dict, Any
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential
from document_client import get_document_client
from document_models import ReceiptExtractionResponse


def extract_receipt_fields(file_path: str, mime_type: str) -> ReceiptExtractionResponse:
    """
    Extracts merchant, tax, total, and items from a receipt using Azure Document Intelligence prebuilt receipt model.
    """
    client = get_document_client("azure_document_intelligence")
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    with open(file_path, "rb") as file:
        poller = client.begin_analyze_document(
            "prebuilt-receipt",
            analyze_request=AnalyzeDocumentRequest(bytes_source=file.read()),
            content_type=mime_type,
            output_content_format=ContentFormat.MARKDOWN
        )
    result = poller.result()

    fields = {
        "merchant": result.documents[0].fields.get("MerchantName", {}).get("content", ""),
        "tax": result.documents[0].fields.get("TotalTax", {}).get("content", ""),
        "total": result.documents[0].fields.get("Total", {}).get("content", ""),
        "items": []
    }

    for item in result.documents[0].fields.get("Items", {}).get("valueArray", []):
        receipt_item = {
            "name": item.get("valueObject", {}).get("Name", {}).get("content", ""),
            "price": item.get("valueObject", {}).get("TotalPrice", {}).get("content", "")
        }
        fields["items"].append(receipt_item)

    return ReceiptExtractionResponse(**fields)