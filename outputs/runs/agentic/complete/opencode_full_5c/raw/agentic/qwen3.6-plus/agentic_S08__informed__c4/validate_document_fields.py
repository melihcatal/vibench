from document_models import (
    validate_invoice_fields,
    validate_receipt_fields,
    REQUIRED_INVOICE_FIELDS,
    REQUIRED_RECEIPT_FIELDS,
    MINIMUM_CONFIDENCE,
    InvoiceExtractionResult,
    ReceiptExtractionResult,
)


def validate_document_fields(extraction_result) -> dict:
    if isinstance(extraction_result, InvoiceExtractionResult):
        result_dict = extraction_result.to_dict()
        return validate_invoice_fields(result_dict)
    elif isinstance(extraction_result, ReceiptExtractionResult):
        result_dict = extraction_result.to_dict()
        return validate_receipt_fields(result_dict)
    else:
        return {
            "valid": False,
            "errors": [f"Unknown document type: {type(extraction_result).__name__}"],
            "confidences": {},
        }


def validate_raw_extraction(result_dict: dict, document_type: str) -> dict:
    if document_type == "invoice":
        return validate_invoice_fields(result_dict)
    elif document_type == "receipt":
        return validate_receipt_fields(result_dict)
    else:
        return {
            "valid": False,
            "errors": [f"Unknown document type: {document_type}"],
            "confidences": {},
        }


def get_validation_summary(validation_result: dict) -> dict:
    is_valid = validation_result.get("valid", False)
    errors = validation_result.get("errors", [])
    confidences = validation_result.get("confidences", {})

    avg_confidence = 0.0
    if confidences:
        avg_confidence = sum(confidences.values()) / len(confidences)

    return {
        "valid": is_valid,
        "error_count": len(errors),
        "errors": errors,
        "field_count": len(confidences),
        "average_confidence": round(avg_confidence, 4),
        "minimum_confidence_threshold": MINIMUM_CONFIDENCE,
    }
