from safety_client import get_comprehend_client
from safety_models import SafetyRequest, SafetyResponse, normalize_response

def moderate_batch(texts):
    client = get_comprehend_client()
    results = []
    for text in texts:
        request = SafetyRequest(text)
        response = client.detect_toxic_content(Text=request.text, LanguageCode='en')
        results.append(normalize_response(response))
    return results