from typing import Dict, Any, Union
from pydantic import ValidationError
from document_models import InvoiceFields, ReceiptFields, ValidationResult


def validate_document_fields(
    extracted_data: Union[InvoiceFields, ReceiptFields],
    confidence_threshold: float = 0.8
) -> Dict[str, Any]:
    validation_result = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": []
    }

    try:
        if isinstance(extracted_data, InvoiceFields):
            if not extracted_data.vendor:
                validation_result["missing_fields"].append("vendor")
                validation_result["is_valid"] = False
            if not extracted_data.date:
                validation_result["missing_fields"].append("date")
                validation_result["is_valid"] = False
            if not extracted_data.total:
                validation_result["missing_fields"].append("total")
                validation_result["is_valid"] = False
            if not extracted_data.line_items:
                validation_result["missing_fields"].append("line_items")
                validation_result["is_valid"] = False

        elif isinstance(extracted_data, ReceiptFields):
            if not extracted_data.merchant:
                validation_result["missing_fields"].append("merchant")
                validation_result["is_valid"] = False
            if not extracted_data.total:
                validation_result["missing_fields"].append("total")
                validation_result["is_valid"] = False
            if not extracted_data.items:
                validation_result["missing_fields"].append("items")
                validation_result["is_valid"] = False

    except ValidationError as e:
        validation_result["is_valid"] = False
        validation_result["missing_fields"].extend([err["loc"][0] for err in e.errors()])

    # Simulate confidence check (in practice, this would come from the provider)
    if hasattr(extracted_data, "_confidence"):
        for field, confidence in extracted_data._confidence.items():
            if confidence < confidence_threshold:
                validation_result["low_confidence_fields"].append(field)
                validation_result["is_valid"] = False

    return ValidationResult(**validation_result).dict()