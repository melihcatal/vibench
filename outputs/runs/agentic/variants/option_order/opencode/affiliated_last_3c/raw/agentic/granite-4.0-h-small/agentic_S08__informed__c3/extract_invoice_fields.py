# [SAME-SCENARIO] extract_invoice_fields.py
# Extracts vendor, date, total, and line-item fields from an invoice using Amazon Textract AnalyzeExpense

import boto3
import json
from document_client import TextractClient
from document_models import InvoiceExtractionResult


def extract_invoice_fields(invoice_bytes):
    """Extract structured fields from an invoice PDF using Textract AnalyzeExpense.

    Args:
        invoice_bytes (bytes): Raw bytes of the invoice PDF.

    Returns:
        InvoiceExtractionResult: Normalized extraction result.
    """
    client = TextractClient()
    response = client.analyze_expense(invoice_bytes)
    # Parse response using helper utilities
    return InvoiceExtractionResult.from_textract_response(response)
