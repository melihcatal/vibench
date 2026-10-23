from typing import Dict, Any

def validate_document_fields(data: Dict[str, Any]) -> bool:
    # Checks required fields and confidence scores (if present)
    required = ["vendor", "date", "total"]
    for field in required:
        if field not in data or not data[field]:
            return False
    # If confidence scores are provided, ensure they exceed a threshold
    if "confidence" in data:
        if data["confidence"] < 0.8:
            return False
    return True
