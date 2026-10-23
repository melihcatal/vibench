from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse

def redact_unsafe(text: str) -> str:
    client = SafetyClient()
    request = SafetyRequest(text)
    response = client.call_api('moderations', request.to_dict())
    safety_response = SafetyResponse(response)
    if not safety_response.is_safe():
        unsafe_spans = safety_response.get_unsafe_spans()
        for span in unsafe_spans:
            start = span['start']
            length = span['length']
            text = text[:start] + '*' * length + text[start + length:]
    return text