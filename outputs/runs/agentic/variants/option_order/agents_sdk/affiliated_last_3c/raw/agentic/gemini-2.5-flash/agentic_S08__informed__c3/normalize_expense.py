import json
from datetime import datetime
from typing import Optional, List, Dict, Any

from document_models import ExpenseDocument, LineItem, ExtractedInvoice, ExtractedReceipt

def normalize_expense(extracted_data: Dict[str, Any], doc_type: str) -> Optional[ExpenseDocument]:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    """
    if doc_type == "invoice":
        invoice_data = ExtractedInvoice(**extracted_data)
        normalized_line_items = [
            LineItem(description=item.get("description", ""), amount=float(item.get("amount", 0.0)))
            for item in invoice_data.line_items
        ]
        return ExpenseDocument(
            document_type="invoice",
            vendor_name=invoice_data.vendor_name,
            document_date=invoice_data.invoice_date,
            total_amount=float(invoice_data.total_amount) if invoice_data.total_amount else 0.0,
            line_items=normalized_line_items,
            currency="USD" # Assuming default for invoices if not extracted
        )
    elif doc_type == "receipt":
        receipt_data = ExtractedReceipt(**extracted_data)
        normalized_line_items = [
            LineItem(
                description=item.get("description", ""),
                amount=float(item.get("total_price", 0.0)) # Mindee's total_price maps to amount
            )
            for item in receipt_data.line_items
        ]
        return ExpenseDocument(
            document_type="receipt",
            vendor_name=receipt_data.merchant_name,
            document_date=None, # Mindee receipt does not always provide a clear date field easily
            total_amount=float(receipt_data.total_amount) if receipt_data.total_amount else 0.0,
            total_tax=float(receipt_data.total_tax) if receipt_data.total_tax else 0.0,
            line_items=normalized_line_items,
            currency=receipt_data.currency if receipt_data.currency else "USD"
        )
    return None
