from typing import Any, Dict, List

from document_models import validate_required_fields


def validate_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = ["vendor", "date", "total"]
    return validate_required_fields(payload, required)
