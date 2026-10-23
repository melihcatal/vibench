from safety_client import get_comprehend_client
from safety_models import SafetyRequest, SafetyResponse, normalize_response

def appeal_translate(text):
    client = get_comprehend_client()
    request = SafetyRequest(text)
    response = client.translate_text(Text=request.text, SourceLanguageCode='en', TargetLanguageCode='es')
    return response['TranslatedText']