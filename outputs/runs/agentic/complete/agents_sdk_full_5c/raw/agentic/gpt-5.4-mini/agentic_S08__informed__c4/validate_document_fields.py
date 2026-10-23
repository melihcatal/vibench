from __future__ import annotations

from typing import Any, Dict, List

from document_models import StructuredDocumentExtractionResponse


REQUIRED_FIELDS = ("vendor", "date", "total")


def validate_document_fields(extracted: StructuredDocumentExtractionResponse) -> Dict[str, Any]:
    missing: List[str] = []
    for field_name in REQUIRED_FIELDS:
        if getattr(extracted, field_name, None) in (None, "", []):
            missing.append(field_name)
    confidence_ok = extracted.confidence is not None and extracted.confidence >= 0.6
    return {
        "valid": not missing and confidence_ok,
        "missing_fields": missing,
        "confidence_ok": confidence_ok,
        "source": "azure-ai-documentintelligence-prebuilt-invoice-receipt",
    }
