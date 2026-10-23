from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse

def moderate_batch(texts: List[str]) -> List[SafetyResponse]:
    client = SafetyClient()
    responses = []
    for text in texts:
        request = SafetyRequest(text)
        response = client.call_api('moderations', request.to_dict())
        responses.append(SafetyResponse(response))
    return responses