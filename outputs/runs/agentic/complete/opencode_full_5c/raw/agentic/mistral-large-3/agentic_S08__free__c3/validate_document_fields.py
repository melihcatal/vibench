from typing import Dict, Any, List, TypedDict


class ValidationResult(TypedDict):
    is_valid: bool
    missing_fields: List[str]
    confidence: float
    errors: List[str]


def validate_document_fields(
    fields: Dict[str, Any], document_type: str
) -> ValidationResult:
    required_fields = {
        "invoice": ["vendor", "date", "total", "line_items"],
        "receipt": ["merchant", "total", "items"],
    }

    missing_fields = []
    errors = []
    confidence = fields.get("confidence", 0.0)

    if document_type not in required_fields:
        raise ValueError(f"Unsupported document type: {document_type}")

    for field in required_fields[document_type]:
        if field not in fields or not fields.get(field):
            missing_fields.append(field)

    if document_type == "invoice":
        if (
            not isinstance(fields.get("line_items", []), list)
            or len(fields.get("line_items", [])) == 0
        ):
            errors.append("Invoice must contain at least one line item")
        if confidence < 0.7:
            errors.append(f"Low confidence score for invoice: {confidence}")

    elif document_type == "receipt":
        if (
            not isinstance(fields.get("items", []), list)
            or len(fields.get("items", [])) == 0
        ):
            errors.append("Receipt must contain at least one item")
        if confidence < 0.7:
            errors.append(f"Low confidence score for receipt: {confidence}")

    if fields.get("total", 0.0) <= 0:
        errors.append("Total amount must be greater than zero")

    return {
        "is_valid": len(missing_fields) == 0 and len(errors) == 0,
        "missing_fields": missing_fields,
        "confidence": confidence,
        "errors": errors,
    }
