from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse

def moderate_text(text: str) -> ModerationResponse:
    client = SafetyClient()
    request = ModerationRequest(text_content=text)
    response = client.moderate_text(request)
    return response
