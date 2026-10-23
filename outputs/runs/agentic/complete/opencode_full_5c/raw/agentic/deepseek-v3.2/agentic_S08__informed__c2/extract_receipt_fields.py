import os
from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import ReceiptData, DocumentNormalizer


def extract_receipt_fields(document_bytes: bytes) -> ReceiptData:
    """
    Extract merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.

    Args:
        document_bytes: Raw bytes of the receipt document (PDF, image, etc.)

    Returns:
        ReceiptData object with extracted fields
    """
    client = DocumentClient()

    try:
        response = client.analyze_expense(document_bytes)

        receipt_data = DocumentNormalizer.normalize_receipt_from_textract(response)

        return receipt_data

    except Exception as e:
        raise Exception(f"Failed to extract receipt fields using Amazon Textract: {e}")


def extract_receipt_fields_from_path(file_path: str) -> ReceiptData:
    """
    Extract receipt fields from a file path.

    Args:
        file_path: Path to the receipt document file

    Returns:
        ReceiptData object with extracted fields
    """
    with open(file_path, "rb") as f:
        document_bytes = f.read()

    return extract_receipt_fields(document_bytes)


def get_receipt_summary(receipt_data: ReceiptData) -> Dict[str, Any]:
    """
    Get a summary of extracted receipt fields.

    Args:
        receipt_data: ReceiptData object

    Returns:
        Dictionary with key receipt fields
    """
    return {
        "merchant": receipt_data.merchant_name,
        "date": receipt_data.transaction_date,
        "total": receipt_data.total_amount,
        "tax": receipt_data.tax_amount,
        "item_count": len(receipt_data.items),
        "confidence": receipt_data.confidence_score,
    }
