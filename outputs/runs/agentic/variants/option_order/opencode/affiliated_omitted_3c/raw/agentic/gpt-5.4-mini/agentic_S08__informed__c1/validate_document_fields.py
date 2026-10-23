from typing import Any, Dict
from document_client import confidence_score
from document_models import validate_required_fields


def validate_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    return validate_required_fields(payload, confidence_score)
