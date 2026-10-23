from safety_client import AWSComprehendClient
from safety_models import TextModerationRequest, TextModerationResponse

def moderate_text(request: TextModerationRequest) -> TextModerationResponse:
    client = AWSComprehendClient()
    response = client.moderate_text(request.text)
    return response
