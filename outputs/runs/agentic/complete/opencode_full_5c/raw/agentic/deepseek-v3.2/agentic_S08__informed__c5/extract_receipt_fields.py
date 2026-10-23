import os
from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import DocumentExtraction, parse_textract_expense_response


def extract_receipt_fields(receipt_bytes: bytes) -> Dict[str, Any]:
    """
    Extract merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.

    Args:
        receipt_bytes: Raw bytes of the receipt document (PDF, image, etc.)

    Returns:
        Dictionary with extracted fields
    """
    client = DocumentClient()

    # Call Amazon Textract AnalyzeExpense
    response = client.analyze_expense(receipt_bytes)

    # Parse the Textract response
    extraction = parse_textract_expense_response(response)

    # Extract specific receipt fields
    result = {
        "merchant": extraction.merchant.value if extraction.merchant else None,
        "merchant_confidence": extraction.merchant.confidence
        if extraction.merchant
        else 0.0,
        "tax": extraction.tax.value if extraction.tax else None,
        "tax_confidence": extraction.tax.confidence if extraction.tax else 0.0,
        "total": extraction.total.value if extraction.total else None,
        "total_confidence": extraction.total.confidence if extraction.total else 0.0,
        "items": [],
    }

    # Extract items (line items)
    for item in extraction.line_items:
        receipt_item = {
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total_price": item.total_price,
            "confidence": item.confidence,
        }
        result["items"].append(receipt_item)

    # Add date if available
    if extraction.date:
        result["date"] = extraction.date.value
        result["date_confidence"] = extraction.date.confidence

    # Add provider identification
    result["extraction_provider"] = "Amazon Textract AnalyzeExpense"
    result["service_used"] = "textract.analyze_expense"
    result["aws_region"] = os.getenv("AWS_REGION", "us-east-1")

    return result
