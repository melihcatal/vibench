from typing import Any, Dict

from document_models import validate_extracted_document


def validate_document_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    return validate_extracted_document(payload)
