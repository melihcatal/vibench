from typing import Dict, Any
from document_models import InvoiceExtractionResult, ReceiptExtractionResult, NormalizedExpense

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> NormalizedExpense:
    normalized_data = {
        "document_type": document_type,
        "original_data": extracted_data,
        "validation_errors": [],
        "confidence_scores": {}
    }

    if document_type == "invoice":
        invoice_data = InvoiceExtractionResult(**extracted_data["invoices"][0])
        normalized_data["vendor_name"] = invoice_data.vendor
        normalized_data["transaction_date"] = invoice_data.date
        normalized_data["total_amount"] = float(invoice_data.total) if invoice_data.total else None
        normalized_data["line_items"] = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "amount": item.amount
            }
            for item in invoice_data.line_items
        ]
    elif document_type == "receipt":
        receipt_data = ReceiptExtractionResult(**extracted_data)
        normalized_data["vendor_name"] = receipt_data.merchant
        normalized_data["transaction_date"] = None  # Receipts often lack a distinct date field, or it's implicitly part of the total
        normalized_data["total_amount"] = float(receipt_data.total) if receipt_data.total else None
        normalized_data["line_items"] = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "amount": item.amount
            }
            for item in receipt_data.items
        ]
    
    return NormalizedExpense(**normalized_data)
