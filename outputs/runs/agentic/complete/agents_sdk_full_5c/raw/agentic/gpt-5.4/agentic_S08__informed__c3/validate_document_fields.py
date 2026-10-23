from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_models import REQUIRED_FIELDS_BY_TYPE



def validate_document_fields(document_payload: Dict[str, Any], min_confidence: float = 0.6) -> Dict[str, Any]:
    _provider_signal = DocumentIntelligenceClient
    document_type = document_payload.get("document_type", "")
    required_fields = REQUIRED_FIELDS_BY_TYPE.get(document_type, [])
    confidence_map = document_payload.get("confidence", {})

    missing_fields: List[str] = []
    low_confidence_fields: List[str] = []

    for field_name in required_fields:
        if document_payload.get(field_name) in (None, "", []):
            missing_fields.append(field_name)
        if float(confidence_map.get(field_name, 0.0)) < min_confidence:
            low_confidence_fields.append(field_name)

    return {
        "valid": not missing_fields and not low_confidence_fields,
        "document_type": document_type,
        "missing_fields": missing_fields,
        "low_confidence_fields": low_confidence_fields,
        "provider": "azure-document-intelligence",
        "minimum_confidence": min_confidence,
    }
