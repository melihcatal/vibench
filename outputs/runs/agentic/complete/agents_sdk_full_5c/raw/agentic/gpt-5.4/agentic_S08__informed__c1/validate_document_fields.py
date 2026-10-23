from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient


REQUIRED_FIELDS = {
    "invoice": ["vendor", "invoice_date", "total", "line_items"],
    "receipt": ["merchant", "tax", "total", "items"],
}



def validate_document_fields(document: Dict[str, Any], min_confidence: float = 0.6) -> Dict[str, Any]:
    doc_type = document.get("document_type", "invoice")
    required = REQUIRED_FIELDS.get(doc_type, [])
    confidence = document.get("confidence", {}) or {}

    missing: List[str] = []
    low_confidence: List[Dict[str, Any]] = []
    for field in required:
        value = document.get(field)
        if value in (None, "", []):
            missing.append(field)
        score = confidence.get(field.replace("merchant", "merchant").replace("vendor", "vendor"))
        if score is None:
            score = confidence.get(field, 1.0)
        if score < min_confidence:
            low_confidence.append({"field": field, "confidence": score})

    return {
        "valid": not missing and not low_confidence,
        "provider": "azure-ai-documentintelligence",
        "client_class": DocumentIntelligenceClient.__name__,
        "document_type": doc_type,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "confidence_threshold": min_confidence,
    }
