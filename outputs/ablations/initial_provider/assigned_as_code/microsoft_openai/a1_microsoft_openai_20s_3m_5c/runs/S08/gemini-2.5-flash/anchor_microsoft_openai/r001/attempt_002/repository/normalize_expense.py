from typing import Dict, Any
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense, LineItem

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> NormalizedExpense:
    confidence_scores = {'overall': 1.0} # Placeholder for actual confidence scores if available
    raw_extraction = extracted_data.copy()

    if document_type == "invoice":
        invoice = ExtractedInvoice(**extracted_data)
        return NormalizedExpense(
            document_type="invoice",
            vendor_name=invoice.vendor,
            transaction_date=invoice.date,
            total_amount=invoice.total,
            currency=invoice.currency,
            line_items=invoice.line_items,
            confidence_scores=confidence_scores,
            raw_extraction=raw_extraction
        )
    elif document_type == "receipt":
        receipt = ExtractedReceipt(**extracted_data)
        return NormalizedExpense(
            document_type="receipt",
            vendor_name=receipt.merchant, # Using merchant as vendor_name for receipts
            transaction_date=None, # Receipt date is not explicitly extracted here, would need to be added to model if required
            total_amount=receipt.total,
            currency=receipt.currency,
            line_items=receipt.items,
            confidence_scores=confidence_scores,
            raw_extraction=raw_extraction
        )
    else:
        raise ValueError(f"Unknown document type: {document_type}")
