from document_models import ExtractedInvoiceFields, ExtractedReceiptFields, NormalizedExpense, LineItem
from typing import Union

def normalize_expense(
    extracted_data: Union[ExtractedInvoiceFields, ExtractedReceiptFields],
    document_type: str
) -> NormalizedExpense:
    
    if document_type == "invoice" and isinstance(extracted_data, ExtractedInvoiceFields):
        return NormalizedExpense(
            document_type="invoice",
            vendor_merchant_name=extracted_data.vendor_name,
            transaction_date=extracted_data.invoice_date,
            total_amount=extracted_data.total_amount,
            line_items=extracted_data.line_items,
            currency="USD", # Assuming USD for now, could be extracted
            tax_amount=None, # Invoices often have tax as part of line items or separate field not covered by current extraction
            note=None,
            confidence_score=1.0 # Placeholder, actual confidence would come from extraction
        )
    elif document_type == "receipt" and isinstance(extracted_data, ExtractedReceiptFields):
        return NormalizedExpense(
            document_type="receipt",
            vendor_merchant_name=extracted_data.merchant_name,
            transaction_date=None, # Receipts often don't have a distinct invoice date, need to find a general date field
            total_amount=extracted_data.total_amount,
            currency="USD", # Assuming USD for now
            line_items=extracted_data.items,
            tax_amount=extracted_data.tax_amount,
            note=None,
            confidence_score=1.0 # Placeholder
        )
    else:
        raise ValueError("Unsupported document type or incorrect data structure provided for normalization.")
