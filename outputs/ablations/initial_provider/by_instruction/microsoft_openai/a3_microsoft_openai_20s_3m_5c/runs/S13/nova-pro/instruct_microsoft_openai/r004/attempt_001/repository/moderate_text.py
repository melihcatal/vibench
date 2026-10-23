from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse

def moderate_text(text: str) -> SafetyResponse:
    client = SafetyClient()
    request = SafetyRequest(text)
    response = client.call_api('moderations', request.to_dict())
    return SafetyResponse(response)