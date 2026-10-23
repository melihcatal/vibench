from __future__ import annotations

from typing import Any, Dict, List

from document_client import require_confidence_threshold


def validate_document_fields(
    normalized_record: Dict[str, Any], min_confidence: float | None = None
) -> Dict[str, Any]:
    threshold = (
        min_confidence if min_confidence is not None else require_confidence_threshold()
    )
    errors: List[str] = []
    warnings: List[str] = []
    if not normalized_record.get("vendor_name"):
        errors.append("vendor_name is required")
    if normalized_record.get("amounts", {}).get("total") is None:
        errors.append("amounts.total is required")
    confidences = normalized_record.get("confidence", {})
    for field_name in ("vendor", "date", "total"):
        score = confidences.get(field_name)
        if score is None:
            warnings.append(f"confidence missing for {field_name}")
        elif score < threshold:
            warnings.append(f"confidence below threshold for {field_name}")
    items = normalized_record.get("items", [])
    if normalized_record.get("document_type") == "invoice" and not items:
        warnings.append("invoice has no line items")
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider": normalized_record.get(
            "source_provider", "azure-document-intelligence"
        ),
    }
