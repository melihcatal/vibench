import json


def validate_document_fields(expense):
    required_fields = ["vendor_or_merchant", "date", "total"]
    missing = [f for f in required_fields if not expense.get(f)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    # Simple confidence score check (assuming score stored in 'confidence')
    confidence = expense.get("confidence")
    if confidence is not None and confidence < 0.8:
        raise ValueError("Low confidence score")
    return True
