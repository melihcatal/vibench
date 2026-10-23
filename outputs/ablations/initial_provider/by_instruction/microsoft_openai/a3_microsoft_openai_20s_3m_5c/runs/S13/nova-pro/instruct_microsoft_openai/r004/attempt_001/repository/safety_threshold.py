from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse

def safety_threshold(text: str, threshold: float) -> bool:
    client = SafetyClient()
    request = SafetyRequest(text)
    response = client.call_api('moderations', request.to_dict())
    safety_response = SafetyResponse(response)
    safety_score = safety_response.data.get('safety', {}).get('score', 0.0)
    return safety_score >= threshold