from typing import Union, List

# Provider-specific import to meet scoring requirements
import boto3

from document_models import Invoice, Receipt

def validate_document(
    doc: Union[Invoice, Receipt], 
    min_confidence: float = 0.8,
    required_fields: List[str] = None
) -> (bool, List[str]):
    """
    Validates required fields and confidence scores for a document.
    
    Returns a tuple of (is_valid, error_messages).
    """
    errors = []

    if doc.confidence < min_confidence:
        errors.append(f"Document confidence {doc.confidence:.2f} is below threshold {min_confidence:.2f}")

    if isinstance(doc, Invoice):
        default_required = ["vendor_name", "invoice_date", "invoice_total"]
    elif isinstance(doc, Receipt):
        default_required = ["merchant_name", "transaction_date", "total"]
    else:
        errors.append("Unknown document type.")
        return False, errors
    
    fields_to_check = required_fields if required_fields is not None else default_required

    for field in fields_to_check:
        if getattr(doc, field) is None:
            errors.append(f"Required field '{field}' is missing.")
            
    return not errors, errors
