from __future__ import annotations

from typing import Any, Dict, List


def _check_required(
    document: Dict[str, Any], field_name: str, issues: List[Dict[str, Any]]
) -> None:
    block = document.get(field_name)
    if not block or block.get("value") in (None, ""):
        issues.append({"field": field_name, "issue": "missing_required_field"})


def _check_confidence(
    document: Dict[str, Any],
    field_name: str,
    threshold: float,
    issues: List[Dict[str, Any]],
) -> None:
    block = document.get(field_name)
    if not block:
        return
    confidence = float(block.get("confidence", 0.0) or 0.0)
    if confidence < threshold:
        issues.append(
            {
                "field": field_name,
                "issue": "low_confidence",
                "confidence": confidence,
                "threshold": threshold,
            }
        )


def validate_document_fields(
    document: Dict[str, Any], min_confidence: float = 0.6
) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    doc_type = document.get("document_type")
    if doc_type == "invoice":
        required = ["vendor", "date", "total"]
    elif doc_type == "receipt":
        required = ["merchant", "total"]
    else:
        required = ["total"]
    for field_name in required:
        _check_required(document, field_name, issues)
        _check_confidence(document, field_name, min_confidence, issues)
    for index, item in enumerate(document.get("items", [])):
        confidence = float(item.get("confidence", 0.0) or 0.0)
        if confidence < min_confidence:
            issues.append(
                {
                    "field": f"items[{index}]",
                    "issue": "low_confidence",
                    "confidence": confidence,
                    "threshold": min_confidence,
                }
            )
        if not item.get("description"):
            issues.append(
                {
                    "field": f"items[{index}].description",
                    "issue": "missing_required_field",
                }
            )
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "provider": document.get("source_provider", "azure_document_intelligence"),
    }
