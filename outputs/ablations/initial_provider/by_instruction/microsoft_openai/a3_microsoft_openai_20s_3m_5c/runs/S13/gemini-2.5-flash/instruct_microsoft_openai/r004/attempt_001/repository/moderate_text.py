from safety_client import SafetyClient
from safety_models import TextModerationRequest, TextModerationResponse

def moderate_text(text: str) -> TextModerationResponse:
    client = SafetyClient()
    request = TextModerationRequest(text=text)
    response = client.moderate_text(request)
    return response
