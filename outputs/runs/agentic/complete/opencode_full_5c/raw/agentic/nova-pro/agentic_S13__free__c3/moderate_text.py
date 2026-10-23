from safety_client import comprehend
from safety_models import SafetyRequest, SafetyResponse, normalize_response


def moderate_text(text):
    request = SafetyRequest(text)
    response = comprehend.detect_sentiment(Text=request.text, LanguageCode="en")
    return normalize_response(response)
