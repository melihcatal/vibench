import os
from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import InvoiceData, DocumentNormalizer


def extract_invoice_fields(document_bytes: bytes) -> InvoiceData:
    """
    Extract vendor, date, total, and line-item fields from an invoice using Amazon Textract AnalyzeExpense.

    Args:
        document_bytes: Raw bytes of the invoice document (PDF, image, etc.)

    Returns:
        InvoiceData object with extracted fields
    """
    client = DocumentClient()

    try:
        response = client.analyze_expense(document_bytes)

        invoice_data = DocumentNormalizer.normalize_invoice_from_textract(response)

        return invoice_data

    except Exception as e:
        raise Exception(f"Failed to extract invoice fields using Amazon Textract: {e}")


def extract_invoice_fields_from_path(file_path: str) -> InvoiceData:
    """
    Extract invoice fields from a file path.

    Args:
        file_path: Path to the invoice document file

    Returns:
        InvoiceData object with extracted fields
    """
    with open(file_path, "rb") as f:
        document_bytes = f.read()

    return extract_invoice_fields(document_bytes)


def get_invoice_summary(invoice_data: InvoiceData) -> Dict[str, Any]:
    """
    Get a summary of extracted invoice fields.

    Args:
        invoice_data: InvoiceData object

    Returns:
        Dictionary with key invoice fields
    """
    return {
        "vendor": invoice_data.vendor_name,
        "date": invoice_data.invoice_date,
        "invoice_number": invoice_data.invoice_number,
        "total": invoice_data.total_amount,
        "tax": invoice_data.tax_amount,
        "subtotal": invoice_data.subtotal,
        "line_item_count": len(invoice_data.line_items),
        "confidence": invoice_data.confidence_score,
    }
