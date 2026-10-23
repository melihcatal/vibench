# [SAME-SCENARIO] validate_document_fields.py
# Validates required structured fields and confidence scores


def validate_document_fields(
    data: dict, required: list[str], confidence_threshold: float = 0.8
) -> bool:
    """Check that required fields are present and have sufficient confidence.

    Parameters:
        data: dict containing extracted fields
        required: list of field names that must be present
        confidence_threshold: minimum confidence (0-1) required

    Returns True if validation passes, False otherwise.
    """
    for field in required:
        value = data.get(field)
        confidence = data.get(f"{field}_confidence", 1.0)
        if not value or confidence < confidence_threshold:
            return False
    return True
