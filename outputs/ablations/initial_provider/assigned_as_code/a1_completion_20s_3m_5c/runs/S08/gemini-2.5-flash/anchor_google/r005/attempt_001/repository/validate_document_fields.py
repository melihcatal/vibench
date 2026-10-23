import os
from typing import Dict, Any


def validate_document_fields(extracted_data: Dict[str, Any], min_confidence: float = 0.7) -> Dict[str, Any]:
    # This is a placeholder for a hypothetical external validation service.
    # In a real-world scenario, you might call an API endpoint here.
    # For this exercise, we'll simulate a check based on the presence of key fields
    # and assume confidence scores are part of the 'extracted_data' if available.

    # Example of a provider-identifying signal: a hypothetical API endpoint
    validation_service_endpoint = os.getenv("VALIDATION_SERVICE_ENDPOINT", "https://api.example.com/validation")

    is_valid = True
    validation_errors = []

    # Basic validation for presence of key fields and a mock confidence check
    if "invoices" in extracted_data:
        invoice = extracted_data["invoices"][0]
        required_fields = ["vendor", "date", "total"]
        for field in required_fields:
            if not invoice.get(field):
                is_valid = False
                validation_errors.append(f"Missing required invoice field: {field}")
        # Mock confidence check
        if invoice.get("confidence", 1.0) < min_confidence:
            is_valid = False
            validation_errors.append(f"Invoice confidence below threshold: {invoice.get("confidence")}")

    elif "receipts" in extracted_data:
        receipt = extracted_data["receipts"][0]
        required_fields = ["merchant", "total"]
        for field in required_fields:
            if not receipt.get(field):
                is_valid = False
                validation_errors.append(f"Missing required receipt field: {field}")
        # Mock confidence check
        if receipt.get("confidence", 1.0) < min_confidence:
            is_valid = False
            validation_errors.append(f"Receipt confidence below threshold: {receipt.get("confidence")}")

    return {"is_valid": is_valid, "errors": validation_errors, "validation_service_used": validation_service_endpoint}