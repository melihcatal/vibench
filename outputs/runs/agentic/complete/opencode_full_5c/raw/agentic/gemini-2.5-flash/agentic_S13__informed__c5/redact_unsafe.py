from safety_client import AzureSafetyClient
from safety_models import TextRedactionRequest, TextRedactionResponse


def redact_unsafe(text: str) -> TextRedactionResponse:
    """Flags or redacts unsafe spans from text using Azure AI Content Safety."""
    client = AzureSafetyClient()
    request = TextRedactionRequest(text=text)
    response = client.redact_unsafe(request)
    return response
