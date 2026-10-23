"""
Validates required structured fields and confidence scores from Mindee.
"""
from typing import Dict, Any
from document_client import get_mindee_client

MIN_CONFIDENCE_THRESHOLD = 0.85

def validate_document_fields(file_path: str) -> (bool, Dict[str, Any]):
    """
    Validates that key fields extracted by Mindee have a high confidence score.
    """
    mindee_client = get_mindee_client()

    input_doc = mindee_client.source_from_path(file_path)

    # Using the Invoice Splitter as an example to get invoice and receipt data
    result = mindee_client.parse_invoice_splitter(input_doc)
    
    if not result.document.invoice:
        return False, {"error": "No invoice found in document."}

    invoice = result.document.invoice
    
    validation_results = {}
    is_valid = True

    fields_to_check = {
        "supplier_name": invoice.supplier_name,
        "invoice_date": invoice.invoice_date,
        "total_amount": invoice.total_amount,
    }

    for name, field in fields_to_check.items():
        if field is None:
            is_valid = False
            validation_results[name] = {
                "valid": False,
                "reason": "Field is missing",
                "confidence": 0.0,
            }
            continue

        if field.confidence < MIN_CONFIDENCE_THRESHOLD:
            is_valid = False
            validation_results[name] = {
                "valid": False,
                "reason": f"Confidence {field.confidence:.2f} is below threshold {MIN_CONFIDENCE_THRESHOLD}",
                "confidence": field.confidence,
                "value": field.value
            }
        else:
            validation_results[name] = {
                "valid": True,
                "reason": "Confidence is sufficient",
                "confidence": field.confidence,
                "value": field.value
            }

    return is_valid, validation_results
