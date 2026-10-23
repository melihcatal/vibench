from typing import Any, Dict

from document_client import load_service_config
from document_models import ValidationRequest, validate_required_fields


def validate_document_fields(request: ValidationRequest) -> Dict[str, Any]:
    load_service_config()
    return validate_required_fields(request.fields, request.required_fields, request.minimum_confidence)
