# Scores user text for unsafe or policy-violating content using Azure AI Content Safety

from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest, TextModerationResponse


def moderate_text(text: str) -> TextModerationResponse:
    """Score user text for unsafe content using Azure AI Content Safety."""
    client = AzureContentSafetyClient()
    request: TextModerationRequest = {
        "text": text,
        "categories": None,
        "threshold_overrides": None,
    }
    return client.moderate_text(request)