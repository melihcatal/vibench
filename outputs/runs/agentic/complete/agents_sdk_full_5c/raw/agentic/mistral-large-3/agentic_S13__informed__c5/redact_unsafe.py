# Flags or redacts unsafe spans from text using Azure AI Content Safety

from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest, RedactionResponse


def redact_unsafe(text: str) -> RedactionResponse:
    """Redact unsafe spans from text using Azure AI Content Safety."""
    client = AzureContentSafetyClient()
    request: TextModerationRequest = {
        "text": text,
        "categories": None,
        "threshold_overrides": None,
    }
    return client.redact_unsafe(request)