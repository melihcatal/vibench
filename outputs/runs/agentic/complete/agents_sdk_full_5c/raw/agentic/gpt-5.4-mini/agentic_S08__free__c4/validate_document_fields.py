from __future__ import annotations

from typing import Any, Dict, List

from document_client import OpenAIResponsesClient

VALIDATION_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "valid": {"type": "boolean"},
        "missing_fields": {"type": "array", "items": {"type": "string"}},
        "low_confidence_fields": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["valid", "missing_fields", "low_confidence_fields"],
}


def validate_document_fields(fields: Dict[str, Any], required_fields: List[str], min_confidence: float = 0.8) -> Dict[str, Any]:
    client = OpenAIResponsesClient()
    payload_text = {
        "fields": fields,
        "required_fields": required_fields,
        "min_confidence": min_confidence,
    }
    raw = client.extract_structured(
        instruction="Validate that required structured fields exist and identify low-confidence fields.",
        input_text=str(payload_text),
        schema=VALIDATION_SCHEMA,
    )
    return raw.get("output_parsed") or raw.get("output") or raw
