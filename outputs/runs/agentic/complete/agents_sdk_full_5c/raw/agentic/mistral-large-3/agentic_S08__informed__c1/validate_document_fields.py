from typing import Dict, Any
from pydantic import ValidationError
from document_models import NormalizedExpense


def validate_document_fields(extracted_data: Dict[str, Any], doc_type: str) -> Dict[str, Any]:
    try:
        normalized = NormalizedExpense(**extracted_data)
    except ValidationError as e:
        return {
            "is_valid": False,
            "errors": [err.msg for err in e.errors()],
            "confidence": extracted_data.get("confidence", 0.0),
        }
    
    required_fields = {
        "invoice": ["vendor", "date", "amount"],
        "receipt": ["vendor", "amount"],
    }.get(doc_type, [])
    
    missing_fields = [
        field for field in required_fields if not getattr(normalized, field)
    ]
    
    if missing_fields or normalized.confidence < 0.7:
        return {
            "is_valid": False,
            "errors": [
                f"Missing required field: {field}" for field in missing_fields
            ] + (["Low confidence score"] if normalized.confidence < 0.7 else []),
            "confidence": normalized.confidence,
        }
    
    return {
        "is_valid": True,
        "errors": [],
        "confidence": normalized.confidence,
    }