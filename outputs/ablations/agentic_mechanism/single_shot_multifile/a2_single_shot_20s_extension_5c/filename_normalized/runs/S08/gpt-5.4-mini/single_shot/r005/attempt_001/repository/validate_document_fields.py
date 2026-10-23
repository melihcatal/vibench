from typing import Any, Dict

from document_models import validate_document_structure


def validate_document_fields(payload: Any) -> Dict[str, Any]:
    return validate_document_structure(payload)
