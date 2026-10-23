from typing import Dict, Any, Optional
from document_models import InvoiceFields, ReceiptFields, NormalizedExpense, LineItem
from forex_python.converter import CurrencyRates

def normalize_expense(extracted_data: Dict[str, Any]) -> NormalizedExpense:
    currency_converter = CurrencyRates()
    
    invoice_fields: Optional[InvoiceFields] = None
    receipt_fields: Optional[ReceiptFields] = None

    if "invoices" in extracted_data and extracted_data["invoices"]:
        invoice_fields = InvoiceFields(**extracted_data["invoices"][0])
    elif "receipts" in extracted_data and extracted_data["receipts"]:
        receipt_fields = ReceiptFields(**extracted_data["receipts"][0])

    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    line_items: List[Dict[str, Any]] = []
    document_type: Optional[str] = None
    confidence_scores: Dict[str, float] = {}
    currency: str = "USD" # Default currency

    if invoice_fields:
        vendor_name = invoice_fields.vendor
        transaction_date = invoice_fields.date
        try:
            total_amount = float(invoice_fields.total) if invoice_fields.total else None
        except ValueError:
            total_amount = None
        document_type = "invoice"
        for item in invoice_fields.line_items:
            line_items.append({"description": item.description, "quantity": item.quantity, "amount": float(item.amount) if item.amount else None})

    elif receipt_fields:
        vendor_name = receipt_fields.merchant
        try:
            total_amount = float(receipt_fields.total) if receipt_fields.total else None
            tax_amount = float(receipt_fields.tax) if receipt_fields.tax else None
        except ValueError:
            total_amount = None
            tax_amount = None
        document_type = "receipt"
        for item in receipt_fields.items:
            line_items.append({"description": item.description, "quantity": item.quantity, "amount": float(item.amount) if item.amount else None})

    # Example of currency conversion (using a hardcoded example, a real scenario would extract currency)
    # if total_amount and currency != "USD":
    #     try:
    #         total_amount = currency_converter.convert(currency, "USD", total_amount)
    #         currency = "USD"
    #     except Exception as e:
    #         print(f"Currency conversion failed: {e}")

    return NormalizedExpense(
        vendor_name=vendor_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=line_items,
        document_type=document_type,
        confidence_scores=confidence_scores
    )
