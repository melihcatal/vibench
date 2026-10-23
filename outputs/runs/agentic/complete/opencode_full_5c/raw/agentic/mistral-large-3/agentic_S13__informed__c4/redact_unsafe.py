from typing import Dict, Optional
from safety_client import TisaneRedactor
from safety_models import RedactionResponse, normalize_redaction_response


def redact_unsafe(text: str, categories: Optional[list] = None) -> RedactionResponse:
    """Redact unsafe spans from text using Tisane API."""
    redactor = TisaneRedactor()
    response = redactor.redact(text, categories)
    return normalize_redaction_response(response)
