import os
from typing import Dict, Any
from document_client import DocumentClient
from document_models import InvoiceFields, parse_textract_expense_response


def extract_invoice_fields(document_bytes: bytes) -> Dict[str, Any]:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using AWS Textract AnalyzeExpense.
    """
    client = DocumentClient()
    response = client.analyze_expense(document_bytes)
    parsed_data = parse_textract_expense_response(response)

    invoice_fields = InvoiceFields(
        vendor_name=parsed_data.get("vendor_name"),
        vendor_address=parsed_data.get("vendor_address"),
        invoice_date=parsed_data.get("invoice_date"),
        invoice_number=parsed_data.get("invoice_number"),
        total_amount=parsed_data.get("total_amount"),
        tax_amount=parsed_data.get("tax_amount"),
        line_items=parsed_data.get("line_items", []),
        confidence=parsed_data.get("confidence"),
    )

    return invoice_fields.model_dump(exclude_none=True)
