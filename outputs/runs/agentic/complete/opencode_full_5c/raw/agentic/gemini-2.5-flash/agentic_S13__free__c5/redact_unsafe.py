from safety_models import RedactionRequest, RedactionResponse
from safety_client import redact_unsafe_with_gcp


def redact_unsafe(text: str) -> RedactionResponse:
    """Flags or redacts unsafe spans from text using Google Cloud Natural Language API for safety detection."""
    request = RedactionRequest(text=text)
    response = redact_unsafe_with_gcp(request)
    return response
