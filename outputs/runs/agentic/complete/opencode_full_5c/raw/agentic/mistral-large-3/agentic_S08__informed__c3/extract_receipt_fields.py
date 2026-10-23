import os
from typing import Dict, Any
from document_client import DocumentClient
from document_models import ReceiptFields, parse_textract_expense_response


def extract_receipt_fields(document_bytes: bytes) -> Dict[str, Any]:
    """
    Extracts merchant, tax, total, and items from a receipt using AWS Textract AnalyzeExpense.
    """
    client = DocumentClient()
    response = client.analyze_expense(document_bytes)
    parsed_data = parse_textract_expense_response(response)

    receipt_fields = ReceiptFields(
        merchant_name=parsed_data.get("vendor_name"),
        merchant_address=parsed_data.get("vendor_address"),
        transaction_date=parsed_data.get("invoice_date"),
        total_amount=parsed_data.get("total_amount"),
        tax_amount=parsed_data.get("tax_amount"),
        items=parsed_data.get("line_items", []),
        confidence=parsed_data.get("confidence"),
    )

    return receipt_fields.model_dump(exclude_none=True)
