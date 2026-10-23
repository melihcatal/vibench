import os
from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import DocumentExtraction, parse_textract_expense_response


def extract_invoice_fields(invoice_bytes: bytes) -> Dict[str, Any]:
    """
    Extract vendor, date, total, and line-item fields from an invoice using Amazon Textract AnalyzeExpense.

    Args:
        invoice_bytes: Raw bytes of the invoice document (PDF, image, etc.)

    Returns:
        Dictionary with extracted fields
    """
    client = DocumentClient()

    # Call Amazon Textract AnalyzeExpense
    response = client.analyze_expense(invoice_bytes)

    # Parse the Textract response
    extraction = parse_textract_expense_response(response)

    # Extract specific invoice fields
    result = {
        "vendor": extraction.vendor.value if extraction.vendor else None,
        "vendor_confidence": extraction.vendor.confidence if extraction.vendor else 0.0,
        "date": extraction.date.value if extraction.date else None,
        "date_confidence": extraction.date.confidence if extraction.date else 0.0,
        "total": extraction.total.value if extraction.total else None,
        "total_confidence": extraction.total.confidence if extraction.total else 0.0,
        "line_items": [],
    }

    # Extract line items
    for item in extraction.line_items:
        line_item = {
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total_price": item.total_price,
            "confidence": item.confidence,
        }
        result["line_items"].append(line_item)

    # Add provider identification
    result["extraction_provider"] = "Amazon Textract AnalyzeExpense"
    result["service_used"] = "textract.analyze_expense"
    result["aws_region"] = os.getenv("AWS_REGION", "us-east-1")

    return result
