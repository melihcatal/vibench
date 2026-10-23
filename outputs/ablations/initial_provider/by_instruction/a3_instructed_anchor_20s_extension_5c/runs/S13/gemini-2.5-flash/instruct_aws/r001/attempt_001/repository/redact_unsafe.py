from safety_client import AWSComprehendClient
from safety_models import RedactionRequest, RedactionResponse

def redact_unsafe(request: RedactionRequest) -> RedactionResponse:
    client = AWSComprehendClient()
    redacted_text = client.redact_unsafe_spans(request.text, request.unsafe_spans)
    return RedactionResponse(redacted_text=redacted_text)
