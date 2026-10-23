from typing import Dict, Any
from document_models import DocumentExtractionResult, NormalizedExpense

def normalize_expense(extraction_result: DocumentExtractionResult) -> NormalizedExpense:
    normalized_data = NormalizedExpense(document_type=extraction_result.document_type)

    # Map common fields
    if "vendor_name" in extraction_result.fields:
        normalized_data.vendor_name = extraction_result.fields["vendor_name"].value
    elif "supplier_name" in extraction_result.fields: # Common for invoices
        normalized_data.vendor_name = extraction_result.fields["supplier_name"].value
    elif "merchant_name" in extraction_result.fields: # Common for receipts
        normalized_data.vendor_name = extraction_result.fields["merchant_name"].value

    if "invoice_date" in extraction_result.fields:
        normalized_data.transaction_date = extraction_result.fields["invoice_date"].value
    elif "receipt_date" in extraction_result.fields:
        normalized_data.transaction_date = extraction_result.fields["receipt_date"].value

    if "total_amount" in extraction_result.fields:
        try:
            normalized_data.total_amount = float(extraction_result.fields["total_amount"].value)
        except (ValueError, TypeError):
            pass
    elif "total_value" in extraction_result.fields: # For receipts
        try:
            normalized_data.total_amount = float(extraction_result.fields["total_value"].value)
        except (ValueError, TypeError):
            pass
    elif "amount" in extraction_result.fields: # For invoices sometimes
        try:
            normalized_data.total_amount = float(extraction_result.fields["amount"].value)
        except (ValueError, TypeError):
            pass

    if "currency" in extraction_result.fields:
        normalized_data.currency = extraction_result.fields["currency"].value
    elif "total_amount" in extraction_result.fields and extraction_result.fields["total_amount"].value:
        # Simple currency extraction if available in total_amount string
        total_val = extraction_result.fields["total_amount"].value
        if total_val and len(total_val) > 0 and not total_val[0].isdigit():
            normalized_data.currency = total_val[0]

    if "tax_amount" in extraction_result.fields:
        try:
            normalized_data.tax_amount = float(extraction_result.fields["tax_amount"].value)
        except (ValueError, TypeError):
            pass

    for item in extraction_result.line_items:
        normalized_data.line_items.append({
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total_price": item.total_price
        })

    # Store raw extraction for auditing/debugging
    normalized_data.raw_extraction = {
        "document_type": extraction_result.document_type,
        "fields": {k: f.__dict__ for k, f in extraction_result.fields.items()},
        "line_items": [li.__dict__ for li in extraction_result.line_items]
    }

    return normalized_data
