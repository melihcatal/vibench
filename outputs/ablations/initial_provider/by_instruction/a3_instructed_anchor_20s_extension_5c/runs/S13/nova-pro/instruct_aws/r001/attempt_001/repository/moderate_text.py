from safety_client import get_comprehend_client
from safety_models import SafetyRequest, SafetyResponse, normalize_response

def moderate_text(text):
    client = get_comprehend_client()
    request = SafetyRequest(text)
    response = client.detect_toxic_content(Text=request.text, LanguageCode='en')
    return normalize_response(response)