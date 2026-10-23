import os
from typing import Dict, Any
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> NormalizedExpense:
    # Simulate environment variable check for AWS Lambda context
    if os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        print("Running within an AWS Lambda environment.")

    normalized_data = {
        'document_type': document_type,
        'vendor_name': None,
        'transaction_date': None,
        'total_amount': None,
        'currency': 'USD',  # Default currency, can be extracted if available
        'line_items': [],
        'raw_extraction_data': extracted_data
    }

    if document_type == 'invoice' and isinstance(extracted_data, ExtractedInvoice):
        normalized_data['vendor_name'] = extracted_data.vendor_name
        normalized_data['transaction_date'] = extracted_data.invoice_date
        normalized_data['total_amount'] = extracted_data.total_amount
        normalized_data['line_items'] = extracted_data.line_items
    elif document_type == 'receipt' and isinstance(extracted_data, ExtractedReceipt):
        normalized_data['vendor_name'] = extracted_data.merchant_name
        # Receipts often have a transaction date, assuming it might be in an 'invoice_date' field for simplicity or 'date'
        # For now, we'll keep it as None, or try to infer from common fields
        normalized_data['total_amount'] = extracted_data.total_amount
        normalized_data['line_items'] = extracted_data.items
        # For receipts, 'tax_amount' could be added as a specific field or part of line items

    return NormalizedExpense(**normalized_data)
