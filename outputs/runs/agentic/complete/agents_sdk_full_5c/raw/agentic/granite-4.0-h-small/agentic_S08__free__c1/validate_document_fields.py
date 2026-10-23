from typing import Dict, Any

def validate_document_fields(doc: Dict[str, Any], required: List[str]) -> bool:
    """
    Validate that all required fields are present and have non-null values.
    Optionally, you could also validate confidence scores (not shown here).
    """
    missing = [f for f in required if f not in doc or doc[f] in (None, "")]
    return len(missing) == 0, missing
