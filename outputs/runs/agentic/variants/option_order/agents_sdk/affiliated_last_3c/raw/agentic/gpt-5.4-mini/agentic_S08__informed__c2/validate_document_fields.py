from __future__ import annotations

from typing import Dict, List

from document_models import REQUIRED_EXPENSE_FIELDS, StructuredDocumentResponse


def validate_document_fields(response: StructuredDocumentResponse) -> Dict[str, object]:
    field_lookup = {field.name: field for field in response.fields}
    missing: List[str] = [name for name in REQUIRED_EXPENSE_FIELDS if name not in field_lookup]
    low_confidence: List[str] = [name for name, field in field_lookup.items() if float(field.confidence or 0.0) < 0.6]
    return {
        "valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "provider": response.provider,
        "model_id": response.model_id,
    }
