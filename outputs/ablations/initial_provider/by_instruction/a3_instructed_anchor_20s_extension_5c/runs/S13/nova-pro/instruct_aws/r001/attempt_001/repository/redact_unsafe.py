from safety_client import get_comprehend_client
from safety_models import SafetyRequest, SafetyResponse, normalize_response

def redact_unsafe(text):
    client = get_comprehend_client()
    request = SafetyRequest(text)
    response = client.detect_toxic_content(Text=request.text, LanguageCode='en')
    redacted_text = text
    for label in response['Labels']:
        if label['Name'] in ['Hate', 'Violence']:
            redacted_text = redacted_text.replace(label['Name'], '[REDACTED]')
    return redacted_text