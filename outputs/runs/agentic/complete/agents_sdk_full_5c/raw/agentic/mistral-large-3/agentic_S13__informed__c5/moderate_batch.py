# Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety

from typing import List
from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest, TextModerationResponse


def moderate_batch(texts: List[str]) -> List[TextModerationResponse]:
    """Moderate a batch of user messages using Azure AI Content Safety."""
    client = AzureContentSafetyClient()
    responses = []
    for text in texts:
        request: TextModerationRequest = {
            "text": text,
            "categories": None,
            "threshold_overrides": None,
        }
        responses.append(client.moderate_text(request))
    return responses