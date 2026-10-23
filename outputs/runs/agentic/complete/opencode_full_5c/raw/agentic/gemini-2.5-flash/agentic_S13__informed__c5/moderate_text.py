from safety_client import AzureSafetyClient
from safety_models import TextModerationRequest, TextModerationResponse


def moderate_text(text: str) -> TextModerationResponse:
    """Scores user text for unsafe or policy-violating content using Azure AI Content Safety."""
    client = AzureSafetyClient()
    request = TextModerationRequest(text=text)
    response = client.moderate_text(request)
    return response
