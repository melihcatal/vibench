from document_models import NormalizedExpense, InvoiceExtractionResult, ReceiptExtractionResult, LineItem
from typing import Dict, Any

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> NormalizedExpense:
    normalized_expense = NormalizedExpense(original_data=extracted_data)

    if document_type == 'invoice':
        invoice_data = InvoiceExtractionResult(**extracted_data)
        normalized_expense.vendor_name = invoice_data.vendor
        normalized_expense.transaction_date = invoice_data.date
        normalized_expense.total_amount = invoice_data.total
        normalized_expense.line_items = invoice_data.line_items
    elif document_type == 'receipt':
        receipt_data = ReceiptExtractionResult(**extracted_data)
        normalized_expense.merchant_name = receipt_data.merchant
        normalized_expense.tax_amount = receipt_data.tax
        normalized_expense.total_amount = receipt_data.total
        normalized_expense.line_items = receipt_data.items
    
    # Add more robust currency extraction, total amount parsing, etc. if needed

    return normalized_expense
