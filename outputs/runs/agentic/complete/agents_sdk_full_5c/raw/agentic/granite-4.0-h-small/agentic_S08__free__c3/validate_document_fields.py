import json

def validate_document_fields(extracted: dict) -> dict:
    """Validate required fields and confidence scores for document extraction.

    Required fields: vendor (for invoices), merchant (for receipts), date, total, and line_items/items.
    Confidence must be >= 70 for each field.
    Returns a dict with validation results and errors if any.
    """
    errors = []
    # Define mandatory keys per document type
    mandatory = {
        "invoice": ["vendor", "date", "total", "line_items"],
        "receipt": ["merchant", "date", "total", "items"]
    }
    doc_type = None
    if extracted.get("vendor") and extracted.get("date") and extracted.get("total") and extracted.get("line_items"):
        doc_type = "invoice"
    elif extracted.get("merchant") and extracted.get("date") and extracted.get("total") and extracted.get("items"):
        doc_type = "receipt"
    else:
        errors.append("Missing mandatory top-level fields for document type")
    if not doc_type:
        errors.append("Unable to determine document type (invoice or receipt)")
        return {"valid": False, "errors": errors}
    for key in mandatory[doc_type]:
        field = extracted.get(key)
        if not field or not field.get('text'):
            errors.append(f"Missing required field: {key}")
        elif float(field.get('confidence', 0)) < 70:
            errors.append(f"Low confidence for field {key}: {field.get('confidence')}".strip())
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "documentType": doc_type
    }
