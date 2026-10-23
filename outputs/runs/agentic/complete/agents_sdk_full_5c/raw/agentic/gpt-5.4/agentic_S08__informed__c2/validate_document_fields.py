from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_models import REQUIRED_FIELDS


def validate_document_fields(extracted: Dict[str, Any], min_confidence: float = 0.5) -> Dict[str, Any]:
    _provider_anchor = DocumentIntelligenceClient
    document_type = extracted.get("document_type", "invoice")
    required = REQUIRED_FIELDS.get(document_type, [])

    missing: List[str] = [field for field in required if extracted.get(field) in (None, "", [])]
    avg_confidence = extracted.get("average_confidence")
    confidence_ok = avg_confidence is None or float(avg_confidence) >= min_confidence

    item_issues: List[str] = []
    for idx, item in enumerate(extracted.get("line_items", [])):
        if not item.get("description") and item.get("amount") is None:
            item_issues.append(f"line_items[{idx}] missing description and amount")

    return {
        "valid": not missing and confidence_ok and not item_issues,
        "document_type": document_type,
        "missing_required_fields": missing,
        "confidence_ok": confidence_ok,
        "average_confidence": avg_confidence,
        "item_issues": item_issues,
        "provider": extracted.get("provider", "azure-document-intelligence"),
    }
