from typing import Dict, Any
from document_models import InvoiceFields, ReceiptFields, NormalizedExpense, LineItem

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> NormalizedExpense:
    if document_type == "invoice":
        invoice_data = InvoiceFields(**extracted_data)
        normalized_line_items = []
        for item in invoice_data.line_items:
            normalized_line_items.append(LineItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total=item.total
            ))

        return NormalizedExpense(
            document_type=document_type,
            vendor_name=invoice_data.vendor_name,
            date=invoice_data.invoice_date,
            total=invoice_data.total_amount,
            currency=invoice_data.currency,
            tax=None, # Invoices typically don't have a single tax field extracted like receipts
            line_items=normalized_line_items,
            raw_data=extracted_data
        )
    elif document_type == "receipt":
        receipt_data = ReceiptFields(**extracted_data)
        normalized_line_items = []
        for item in receipt_data.line_items:
            normalized_line_items.append(LineItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total=item.total
            ))

        return NormalizedExpense(
            document_type=document_type,
            vendor_name=receipt_data.merchant_name,
            date=receipt_data.transaction_date,
            total=receipt_data.total_amount,
            currency=receipt_data.currency,
            tax=receipt_data.tax_amount,
            line_items=normalized_line_items,
            raw_data=extracted_data
        )
    else:
        raise ValueError("Unsupported document type for normalization.")
