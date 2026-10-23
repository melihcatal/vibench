from safety_client import get_comprehend_client
from safety_models import SafetyRequest, SafetyResponse, normalize_response

def safety_threshold(text, threshold=0.5):
    client = get_comprehend_client()
    request = SafetyRequest(text)
    response = client.detect_toxic_content(Text=request.text, LanguageCode='en')
    for label in response['Labels']:
        if label['Score'] > threshold:
            return False
    return True