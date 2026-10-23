# extract_invoice_fields.py
# [SAME-SCENARIO] Textract AnalyzeExpense integration
import boto3
import json
from document_client import DocumentClient

# AWS credentials are read from environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
client = boto3.client("textract")


def extract_invoice_fields(document_bytes):
    """Extract vendor, date, total, and line-item fields from an invoice using Amazon Textract AnalyzeExpense.

    Args:
        document_bytes (bytes): The binary content of the invoice PDF/JPEG.

    Returns:
        dict: Normalized invoice fields.
    """
    response = client.analyze_expense(Document={"Bytes": document_bytes})
    # Use DocumentClient to parse and normalize the raw response
    normalized = DocumentClient.normalize_expense_response(response)
    return normalized
