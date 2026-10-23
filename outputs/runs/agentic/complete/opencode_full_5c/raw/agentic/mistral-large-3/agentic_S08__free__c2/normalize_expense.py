from typing import Dict, Any
from document_models import NormalizedExpense, normalize_document_fields


def normalize_expense(
    extracted_fields: Dict[str, Any], document_type: str
) -> NormalizedExpense:
    """Normalize extracted expense fields into a standard JSON schema."""
    return normalize_document_fields(extracted_fields, document_type)
