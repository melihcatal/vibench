# [SAME-SCENARIO] extract_receipt_fields.py
"""
Extract merchant, tax, total, and items from a receipt using Azure Form Recognizer.
"""
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from document_models import ReceiptExtractionRequest, ReceiptExtractionResponse

def extract_receipt_fields(receipt_path: str) -> ReceiptExtractionResponse:
    """Extract structured fields from a receipt image.

    Args:
        receipt_path: Path to the receipt image file.

    Returns:
        ReceiptExtractionResponse containing merchant, tax, total, and items.
    """
    # Use connection string from environment variable (provider-specific)
    endpoint = "https://<YOUR_RESOURCE_NAME>.cognitiveservices.azure.com/"
    credential = "<YOUR_KEY>"
    client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)
    # Analyze the receipt document
    with open(receipt_path, "rb") as file:
        poller = client.begin_analyze_document("prebuilt/receipt", file)
        result = poller.result()
    # Extract fields (placeholder parsing logic)
    vendor = result.fields["Merchant"].copy_from_result().value if "Merchant" in result.fields else "Unknown"
    tax = result.fields["Tax"].copy_from_result().value if "Tax" in result.fields else 0.0
    total = result.fields["Total"] .copy_from_result().value if "Total" in result.fields else 0.0
    items = []
    for item in result.selections["items"]:
        items.append({"description": item.text, "price": 0.0})  # placeholder values
    return ReceiptExtractionResponse(vendor=vendor, tax=tax, total=total, items=items)
