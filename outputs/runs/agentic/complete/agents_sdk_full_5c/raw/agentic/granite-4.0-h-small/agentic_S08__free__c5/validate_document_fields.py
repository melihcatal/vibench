from typing import Dict, Any

def validate_document_fields(extracted: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate that the extracted document contains all required fields and that
    confidence scores meet a minimum threshold (e.g., 0.8).
    """
    required_fields = schema.get("required", [])
    min_confidence = schema.get("min_confidence", 0.8)

    # Check required top-level fields
    for field in required_fields:
        if field not in extracted or not extracted[field]:
            print(f"Missing required field: {field}")
            return False

    # Check confidence scores (assume numeric field named 'confidence')
    confidence = extracted.get("confidence", 0.0)
    if confidence < min_confidence:
        print(f"Confidence {confidence:.2f} below threshold {min_confidence}")
        return False

    return True