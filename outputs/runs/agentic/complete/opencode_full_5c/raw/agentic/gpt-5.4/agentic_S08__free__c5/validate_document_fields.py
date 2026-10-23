from __future__ import annotations

from typing import Any, Dict, List

from document_models import ValidationResult


REQUIRED_FIELDS = {
    "invoice": ["vendor", "invoice_date", "total", "line_items"],
    "receipt": ["merchant", "total", "line_items"],
}


def validate_document_fields(
    extracted_fields: Dict[str, Any], minimum_confidence: float = 0.6
) -> Dict[str, Any]:
    document_type = extracted_fields.get("document_type", "invoice")
    confidence_scores = extracted_fields.get("confidence_scores", {})
    missing_fields: List[str] = []
    low_confidence_fields: List[str] = []
    for field in REQUIRED_FIELDS.get(document_type, []):
        value = extracted_fields.get(field)
        if value in (None, "") or value == []:
            missing_fields.append(field)
        if (
            confidence_scores.get(
                field, confidence_scores.get(field.replace("line_items", "items"), 0.0)
            )
            < minimum_confidence
        ):
            low_confidence_fields.append(field)
    result = ValidationResult(
        valid=not missing_fields and not low_confidence_fields,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        normalized={
            "provider": "azure-document-intelligence",
            "document_type": document_type,
            "confidence_threshold": minimum_confidence,
        },
    )
    return result.to_dict()
