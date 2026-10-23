import os
from safety_client import ContentSafetyClient
from safety_models import RedactionRequest, RedactionResponse

def redact_unsafe(request: RedactionRequest, config=None) -> RedactionResponse:
    # Google Cloud Content Safety API would be the provider for actual redaction.
    # For this example, the ContentSafetyClient contains a mock implementation.
    client = ContentSafetyClient(project_id=config.get("project_id") if config else None)

    redacted_content, redacted_spans = client.redact_unsafe(request.text, request.threshold)

    return RedactionResponse(
        original_text=request.text,
        redacted_text=redacted_content,
        redacted_spans=redacted_spans
    )
