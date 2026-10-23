# [SAME-SCENARIO] validate_document_fields.py

# Validates required fields and confidence scores for document extractions
import re
from document_models import ExtractionResult


def validate_document_fields(result: ExtractionResult) -> bool:
    """Validate that required fields exist and score confidence >= 0.7.

    Returns True if validation passes, False otherwise.
    """
    required = {
        "invoice": ["vendor", "date", "total", "line_items"],
        "receipt": ["merchant", "tax", "total", "items"],
    }
    schema = required.get(result.document_type)
    if not schema:
        raise ValueError(f"Unsupported document_type: {result.document_type}")
    # Simple validation logic
    if not result.confidence >= 0.7:
        return False
    for field in schema:
        if not getattr(result, field):
            return False
    return True
