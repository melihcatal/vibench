from typing import List
from safety_client import AzureSafetyClient
from safety_models import TextModerationRequest, TextModerationResponse


def moderate_batch(texts: List[str]) -> List[TextModerationResponse]:
    """Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety."""
    client = AzureSafetyClient()
    requests = [TextModerationRequest(text=text) for text in texts]
    responses = client.moderate_batch(requests)
    return responses
