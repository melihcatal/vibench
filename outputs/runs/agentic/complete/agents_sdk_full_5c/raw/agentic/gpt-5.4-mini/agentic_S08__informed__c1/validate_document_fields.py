from __future__ import annotations

from typing import Dict, List

from document_models import DocumentExtractionResponse


REQUIRED_FIELDS = ("vendor", "date", "total")
MIN_CONFIDENCE = 0.7


def validate_document_fields(response: DocumentExtractionResponse) -> Dict[str, List[str]]:
    missing = [name for name in REQUIRED_FIELDS if name not in response.fields]
    low_confidence = [name for name, field in response.fields.items() if field.confidence < MIN_CONFIDENCE]
    return {"missing": missing, "low_confidence": low_confidence}
