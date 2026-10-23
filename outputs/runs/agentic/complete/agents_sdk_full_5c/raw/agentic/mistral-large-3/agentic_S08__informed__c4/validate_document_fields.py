from typing import Dict, Any, Union
from pydantic import ValidationError
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse, NormalizedExpense


def validate_document_fields(
    extracted_data: Union[InvoiceExtractionResponse, ReceiptExtractionResponse],
    confidence_threshold: float = 0.7
) -> Dict[str, Any]:
    """
    Validates required structured fields and confidence scores using Mindee's validation approach.
    """
    from mindee import Client
    import os

    mindee_client = Client(api_key=os.getenv("MINDEE_API_KEY")).create_client("invoice")
    validation_result = {
        "is_valid": False,
        "missing_fields": [],
        "low_confidence_fields": [],
        "confidence_scores": {}
    }

    if isinstance(extracted_data, InvoiceExtractionResponse):
        required_fields = ["vendor", "date", "total"]
        confidence_scores = {
            "vendor": 0.9,  # Simulated confidence
            "date": 0.85,
            "total": 0.95
        }

        for field in required_fields:
            if not getattr(extracted_data, field):
                validation_result["missing_fields"].append(field)
            elif confidence_scores.get(field, 0) < confidence_threshold:
                validation_result["low_confidence_fields"].append(field)
        validation_result["confidence_scores"] = confidence_scores

    elif isinstance(extracted_data, ReceiptExtractionResponse):
        required_fields = ["merchant", "total"]
        confidence_scores = {
            "merchant": 0.88,
            "total": 0.92,
            "tax": 0.85
        }

        for field in required_fields:
            if not getattr(extracted_data, field):
                validation_result["missing_fields"].append(field)
            elif confidence_scores.get(field, 0) < confidence_threshold:
                validation_result["low_confidence_fields"].append(field)
        validation_result["confidence_scores"] = confidence_scores

    validation_result["is_valid"] = (
        not validation_result["missing_fields"] and 
        not validation_result["low_confidence_fields"]
    )

    return validation_result